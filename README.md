![bliksem](https://github.com/user-attachments/assets/f009f81d-2160-4878-94f8-199f6805eb8f)

# Bliksem Smart Home IoT Scanner
Bliksem is a home IoT scanner which aims to reduce the prevalence of threats in smart homes. The tool is a preventative measure that can be run on any device with python installed. It will scan your entire home subnet and external IP address. 

## Features
* Internal subnet scan
* External IP address scan
* MAC address lookup to discover vendors of IoT devices
* Brute force of open telnet ports to find default or weak logins
* Shodan scan of external IP if API key is used
* Reccomendations and summary files created to highlight important security flaws

## Usage
In order to run the script with full functionality, follow the below steps:
1. Clone the repository:
```bash
git clone https://github.com/askaari-cyber/bliksem.git
```
2. Install the requirements
```bash
pip install -r requirements.txt
```
3. Run the script
```bash
python bliksem.py
```
Or to run with Shodan:
```bash
python bliksem.py -a [shodan api]
```
4. Wait for the scan to complete and review the generated reports.

## Contributing
Contrbutions are welcome! Please submit a pull request or suggest improvements/new features by opening an issue. 


## Disclaimer
Always ensure thorough testing before using in any critical or production environments.
