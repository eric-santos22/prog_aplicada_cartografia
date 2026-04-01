from pathlib import Path
import requests, os

class Downloader:
    """
    Class that downloads a file from a certain URL and saves it on a given directory
    
    Args:
        url: url to get data
        destination_directory: folder that file will be saved
    """
    
    def __init__(self, url: str, destination_directory: Path, file_name: str | None = None):
        self.url = url
        self.dir = Path(destination_directory)
        self.file_name = file_name if file_name != "" else None
        os.makedirs(self.dir, exist_ok=True)

    def _get_destination_path(self):
        if self.file_name is None:
            name = self.url.split("/")[-1]
        else:
            name = self.file_name
        destination_path =  self.dir.joinpath(name)
        return destination_path
    
    def download_file(self, progress_callback=None):
        destination_path =  self._get_destination_path()
        with requests.get(self.url, stream=True) as response:
            response.raise_for_status()
            total_size = response.headers.get('content-length')
            if total_size:
                total_size = int(total_size)
            downloaded = 0
            with open(destination_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(downloaded, total_size)

if __name__ == "__main__":
    url = "https://geoftp.ibge.gov.br/cartas_e_mapas/folhas_topograficas/vetoriais/escala_100mil/projeto_ba100/itapicuru1792/a_vbd_lcar.zip"
    path = Path("C:/Users/ericd/Proj Cart/prog_aplicada_cartografia/downloader_project")
    
    download = Downloader(url, path).download_file()


