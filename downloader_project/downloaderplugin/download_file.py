from pathlib import Path
import requests, os
import warnings
import loguru as log

class Downloader:
    """
    Class that downloads a file from a certain URL and saves it on a given directory
    
    Args:
        url: url to get data
        destination_directory: folder that file will be saved
    """
    
    def __init__(self, url: str, destination_directory: Path):
        self.url = url
        self.dir = Path(destination_directory)
        os.makedirs(self.dir, exist_ok=True)

    def _status(self, response: requests.Response, response_code):
        match response_code:
            case 200:
                log.logger.success("Successfull request")
            case 404:
                log.logger.warning("404: url returns nothing")
                response.raise_for_status()
            case 500:
                warnings.warn("500: server raised error")
                response.raise_for_status()
            case _:
                print(f"Received unexpected status: {response_code}")

    def download_file(self):
        response = requests.get(self.url, stream=True)
        self._status(response, response.status_code)
        name = self.url.split("/")[-1]
        destination_path =  self.dir / name

        with open(destination_path, "wb") as file:
            file.write(response.content)
            log.logger.success("File Downloaded Succefully")

if __name__ == "__main__":
    url = "https://geoftp.ibge.gov.br/cartas_e_mapas/folhas_topograficas/vetoriais/escala_100mil/projeto_ba100/itapicuru1792/a_vbd_lcar.zip"
    path = Path("C:/Users/ericd/Proj Cart/prog_aplicada_cartografia/downloader_project")
    
    download = Downloader(url, path).download_file()


