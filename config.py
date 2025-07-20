from dotenv import load_dotenv
import os

load_dotenv()

shodan_key = os.getenv('SHODAN_API_KEY')
safe_browsing_key=os.getenv('SAFE_BROWSING_KEY')
virustotal_key=os.getenv('VIRUSTOTAL_KEY')


