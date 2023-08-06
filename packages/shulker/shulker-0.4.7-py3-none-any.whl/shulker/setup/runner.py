import urllib.request, json
import subprocess

class Runner():
    def __init__(self, verbose=False):
        self.jar_name = 'server.jar'
        self.version_manifest = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
        self.verbose = verbose
        self.stdout = subprocess.DEVNULL if not self.verbose else 1
        self.stderr = subprocess.DEVNULL if not self.verbose else 2

    def run(self):
        print("Browsering minecraft versions...")
        latest_url = self.browse_mc_versions()
        print("Getting latest version...")
        latest_version_info = self.get_jar_from_url(latest_url)
        print("Downloading latest version...")
        self.download_jar_and_generate(latest_version_info)
        print("Parsing jar...")
        self.parse_jar()
        print("Moving .json...")
        self.move_json()
        print("Cleaning up...")
        self.clean_up()

    def clean_up(self):
        instructions = [
            f'rm -rf {self.jar_name}',
            f'rm -rf logs',
            f'rm -rf generated',
            f'rm -rf libraries',
            f'rm -rf test',
            f'rm -rf versions'
        ]
        for instruction in instructions:
            subprocess.run(instruction.split(" "), stdout=self.stdout, stderr=self.stdout)
    
    def move_json(self):
        instructions = [
            f'mv ./generated/reports/blocks.json ../functions/mc_data/block_list.json',
            f'mv ./generated/reports/commands.json ../functions/mc_data/commands.json',
            f'mv ./generated/reports/registries.json ../functions/mc_data/registries.json',
        ]
        for instruction in instructions:
            subprocess.run(instruction.split(" "), stdout=self.stdout, stderr=self.stdout)
        
    def parse_jar(self):
        cmd = 'java -DbundlerMainClass=net.minecraft.data.Main -jar server.jar --all'.split(" ")
        subprocess.run(cmd, stdout=self.stdout, stderr=self.stdout)

    def download_jar_and_generate(self, url):
        download = f'wget {url} -O {self.jar_name}'.split(" ")
        subprocess.run(download, stdout=self.stdout, stderr=self.stdout)

    def get_jar_from_url(self, latest_url):
        with urllib.request.urlopen(latest_url) as url:
            latest_version_info = json.loads(url.read().decode())
            return latest_version_info['downloads']['server']['url']

    def browse_mc_versions(self):
        with urllib.request.urlopen(self.version_manifest) as url:
            server_jar_version_list = json.loads(url.read().decode())
            latest_version = server_jar_version_list["latest"]["release"]
            
            for version in server_jar_version_list["versions"]:
                if version['id'] == latest_version:
                    latest_url = version['url']
                    return latest_url

if __name__ == '__main__':
    tasks = Runner(verbose=True)
    tasks.run()

