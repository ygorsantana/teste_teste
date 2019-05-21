from backend.models.ftp_downloader.download import download_file
from backend.models.productsCorello.update import write_on_database

download_file('rappi.corello_oscarfreire')
write_on_database(4)