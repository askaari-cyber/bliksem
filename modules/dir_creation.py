import datetime
import os


class Creation:
    @staticmethod
    def make_dir():
        structure = False
        current_day = datetime.datetime.now().date()

        dirs = [f'./Scan_results_{current_day}/',
                f'./Scan_results_{current_day}/Nmap/',
                f'./Scan_results_{current_day}/Brute_force/',
                f'./Scan_results_{current_day}/Details/',
                f'./Scan_results_{current_day}/Key_findings/']

        for dirc in dirs:
            if not os.path.exists(dirc):
                structure = True
                os.makedirs(dirc)

        return structure
