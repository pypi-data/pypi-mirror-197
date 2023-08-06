"""
Importer postnr fra postens offisielle URL.
"""
import sys, os
import time
import traceback
import requests
import argparse
import django;django.setup()
from django import template
from dknorway.models import Kommune, PostSted
from dknorway import __version__
import dknorway
from django_extensions.management.jobs import MonthlyJob
from dk.collections import pset
from dkddog import Fido
fido = Fido('dknorway.import_postnummer')

CURDIR = os.path.dirname(__file__)
SRCDIR = os.path.dirname(dknorway.__file__)
DATAFILE_URL = "http://www.bring.no/radgivning/sende-noe/adressetjenester/postnummer/_attachment/615728?_ts=14fd0e1cc58?_download=true"
DATAFILE_DIR = os.path.join(SRCDIR, 'data')
DATAFILE = os.path.join(DATAFILE_DIR, 'postnrdata.txt')
ENCODING = 'utf-8'


class NoData(Exception):
    """No data to process.
    """


def split_line(line):
    return [item.strip() for item in line.split('\t')]


def datafile_exists():
    if not os.path.exists(DATAFILE_DIR):
        os.mkdir(DATAFILE_DIR)
    return os.path.exists(DATAFILE)
    

def write_datafile(txt):
    datafile_exists()
    with open(DATAFILE, 'wb') as fp:
        fp.write(txt.encode(ENCODING))


def read_datafile():
    datafile_exists()
    with open(DATAFILE, 'rb') as fp:
        return fp.read().decode(ENCODING)    


def has_datafile_changed(txt):
    if not datafile_exists():
        # write_datafile(txt)
        return True

    previous = read_datafile()
    changed = previous != txt
    # if changed:
    #    write_datafile(txt)
    return changed


def fetch_datafile(args):
    """Download data file.
    """
    r = requests.get(DATAFILE_URL)
    txt = r.text
    if args.force or has_datafile_changed(txt):
        lines = txt.splitlines()  # r.text is unicode
        for line in lines:
            postnr, sted, kkode, knavn, _ = split_line(line)
            yield postnr, sted, kkode, knavn

        write_datafile(txt)
    elif args.verbose:
        fido.info_event(
            "Finished fetching datafile",
            "Data has not changed since last run."
        )
        print("data has not changed since last run (use --force to override)")
        raise NoData()


def create_postnrcache_py(postnr):
    postnrs = [int(p) for p in sorted(set(postnr))]
    with open(os.path.join(CURDIR, 'postnrcache.pytempl')) as fp:
        t = template.Template(fp.read().decode('u8'))
    
    with open(os.path.join(SRCDIR, 'postnrcache.py'), 'w') as fp:
        fp.write(unicode(t.render(template.Context(locals()))).encode('u8'))


def mark_inactive(args, poststeds):
    for p in poststeds:
        if args.verbose:
            print("marking as inactive:", p.postnummer)
        p.active = False
        p.save()


def add_and_update_poststeds(args, lines, postnr_poststed, knr_kommune):
    def get_coordinates(csvfile):
        import csv
        coordinates = {}
        with open(csvfile) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                coordinates[row[0]] = (row[9], row[10])
        return coordinates
    
    coordinates = get_coordinates(os.path.join(CURDIR, 'postnummer.csv'))
    
    def get_kommune(kode, navn):
        if kode not in knr_kommune:
            if args.verbose:
                print("new kommune:", kode, navn)
            knr_kommune[kode] = Kommune.objects.create(kode=kode, navn=navn)
        return knr_kommune[kode]
    
    for postnr, sted, kkode, knavn in lines:
        print(postnr, sted, kkode, knavn, postnr in postnr_poststed)
        if postnr in postnr_poststed:  # update existing poststed
            p = postnr_poststed[postnr]
            lat, lon = coordinates[postnr.encode('u8').lstrip('0')]
            print(lat,lon)
            
            if not p.active:
                p.delete()
                postnr_poststed[postnr] = PostSted.objects.create(
                    postnummer=postnr,
                    poststed=sted,
                    kommune=get_kommune(kode=kkode, navn=knavn),
                    lat=lat,
                    lng=lon,
                    
                )
                continue
            
            if lat != p.lat:
                p.lat = lat
                p.lng = lon
                p.save()
                if args.verbose:
                    print("updated poststed:", postnr, sted)
                

            if sted != p.poststed:
                p.poststed = sted
                p.save()
                if args.verbose:
                    print("updated poststed:", postnr, sted)

            if not p.kommune:
                p.kommune = get_kommune(kode=kkode, navn=knavn)
                p.save()
                if args.verbose:
                    print("poststed was missing kommune:", p)
                
            if kkode != p.kommune.kode  or knavn != p.kommune.navn:
                p.kommune.kode = kkode
                p.kommune.navn = knavn
                p.kommune.save()
                if args.verbose:
                    print("updated kommune:", postnr, sted, knavn)
        
        else:  # new poststed
            postnr_poststed[postnr] = PostSted.objects.create(
                postnummer=postnr,
                poststed=sted,
                kommune=get_kommune(kode=kkode, navn=knavn),
                lat=lat,
                lng=lon,
            )
            if args.verbose:
                print("created new poststed:", postnr, sted, kkode, knavn)


def process_new_file(args):
    try:
        lines = list(fetch_datafile(args))
        current_poststed = PostSted.objects.all()
        current_kommune = Kommune.objects.filter(active=True)
        current_postnr = {p.postnummer for p in current_poststed if p.active}
        new_postnrs = {line[0] for line in lines}

        inactive_postnr = current_postnr - new_postnrs
        postnr_poststed = {p.postnummer: p for p in current_poststed}
        inactive_poststed = [postnr_poststed[postnr] for postnr in sorted(inactive_postnr)]
        mark_inactive(args, inactive_poststed)
        for p in inactive_poststed:
            del postnr_poststed[p.postnummer]
        
        add_and_update_poststeds(
            args, 
            lines, 
            postnr_poststed,                        # will be updated
            {k.kode: k for k in current_kommune}
        )
        create_postnrcache_py(PostSted.objects.filter(active=True).values_list('postnummer', flat=True))
        fido.info_event(
            "Finished processing file",
        )
        
    except NoData:
        pass


class Job(MonthlyJob):
    help = "Import postnrs. from bring."
    
    def execute(self):      # you shouldn't need to change this method
        start = time.time()
        fido.info_event('started')
        
        args = pset(verbose=0, force=1)
        
        try:
            process_new_file(args)
            fido.service_ok()
        except:
            fido.service_critical(traceback.format_exc())
        else:
            fido.success_event('finished')
            fido.report_duration(time.time() - start)


def main(args=None):
    start = time.time()
    args = args or sys.argv[1:]
    p = argparse.ArgumentParser()
    p.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    p.add_argument('--verbose', '-v', action='store_true', help='verbose output')
    p.add_argument('--force', '-f', action='store_true', help='force processing')

    args = p.parse_args(args)
    if args.verbose:
        print("starting insert..")
    process_new_file(args)
    if args.verbose:
        print("finished:", time.time() - start)


if __name__ == "__main__":
    main()
