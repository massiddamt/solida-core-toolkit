#!/usr/bin/env python3

import os
import sys
import argparse
import ftplib
import logging


class App(object):
    def __init__(self, args=None, logger=None):
        self.logger = logger
        self.reference_dir = args.reference_dir #if args.reference_dir else os.getcwd()
        self.release = args.release
        self.force = args.force
        if os.path.exists(os.path.join(self.reference_dir,"ucsc",self.release)):
            if not self.force:
                raise ValueError("WARNING: Folder exists. Rerun with the flag '--force'")
            self.logger.info("ALERT: '--force' flag activated: using existing folder")
        else:
            self.logger.info("Creating reference folder tree at {}".format(self.reference_dir))
            #os.mkdir(self.reference_dir)
            os.makedirs(os.path.join(self.reference_dir,"ucsc",self.release,"known_variants"))

    def ftp_download(self):

        def exec_ftp(search_pattern=None,download_path=None):
            i=search_pattern
            for filename in ftp.nlst(i):
                if filename not in downloaded:
                    self.logger.info("Downloading {} ".format(filename))
                    fhandle = open(os.path.join(download_path,filename), 'wb')
                    print('Getting ' + filename)
                    ftp.retrbinary('RETR ' + filename, fhandle.write)
                    fhandle.close()
                    self.logger.info("{}: download complete!".format(filename))
                    downloaded.append(filename)
                else:
                    continue

        try:
            ftp = ftplib.FTP("ftp.broadinstitute.org", "gsapubftp-anonymous", "")
        except ftplib.all_errors as e:
            self.logger.info("ERROR: {} ".format(e))
            self.logger.info("TRY AGAIN")

        ftp.cwd(os.path.join("bundle",self.release))

        downloaded = []

        if self.release == "hg19":
            exec_ftp(search_pattern="ucsc*",download_path=os.path.join(self.reference_dir,"ucsc",self.release))
        else:
            exec_ftp(search_pattern="Homo_sapiens*", download_path=os.path.join(self.reference_dir, "ucsc", self.release))

        known_list = ["1000G_*", "Mills_and_1000G_gold*", "dbsnp*", "hapmap_3.3.*"]

        for i in known_list:
            exec_ftp(search_pattern=i, download_path=os.path.join(self.reference_dir, "ucsc", self.release,"known_variants"))
#        ftp.quit()

        self.logger.info("Downloaded {} files:".format(str(len(downloaded))))
        for downloaded_element in downloaded:
            self.logger.info(downloaded_element)


def get_logger(name, level="WARNING", filename=None, mode="a"):
    log_format = '%(asctime)s|%(levelname)-8s|%(name)s |%(message)s'
    log_datefmt = '%Y-%m-%d %H:%M:%S'
    logger = logging.getLogger(name)
    if not isinstance(level, int):
        try:
            level = getattr(logging, level)
        except AttributeError:
            raise ValueError("unsupported literal log level: %s" % level)
        logger.setLevel(level)
    if filename:
        handler = logging.FileHandler(filename, mode=mode)
    else:
        handler = logging.StreamHandler()
    formatter = logging.Formatter(log_format, datefmt=log_datefmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def make_parser():
    parser = argparse.ArgumentParser(description='Prepare reference files for solida-core pipelines')

    parser.add_argument('--reference_dir', '-w', metavar="PATH", required=True,
                        help="Destination folder for reference files")

    parser.add_argument('--release', '-r', required=True,
                        help="UCSC Genome Release to download: [hg19,hg38]")

    parser.add_argument('--force', action='store_true',
                        help="Write merged fastq files in the directory even if it exists (Default: FALSE)")

    return parser


def main(argv):
    parser = make_parser()
    args = parser.parse_args(argv)

    # Initializing logger
    logger = get_logger('main', level='INFO')
    workflow = App(args=args, logger=logger)

    workflow.ftp_download()


if __name__ == '__main__':
    main(sys.argv[1:])