import os
import requests
import time
import logging

http_api_token = os.getenv('HTTP_API_TOKEN')
if not http_api_token:
    raise Exception('HTTP_API_TOKEN env not found')

chat_id = os.getenv('CHAT_ID')
if not chat_id:
    raise Exception('CHAT_ID env not found')

telegram_base_url=f"https://api.telegram.org/bot{http_api_token}"

validation_url="https://pronto.blumenau.sc.gov.br/pronto/agendamentovacinacaointerno.aspx"

log = logging.getLogger('fuck_app')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
wait_when_change_minutes=1

def send_message(message):
    return requests.post(
            url=f"{telegram_base_url}/sendMessage",
            data={"chat_id": chat_id, "text": message},
            timeout=2
        ).json()

def do_i_need_to_kill_the_president():
    try:
        current_status_response = requests.get(
                url=validation_url,
                allow_redirects=False,
                timeout=2
            )

        vaccines_only_for_entrepreneurs = current_status_response and \
            current_status_response.status_code == 301 and \
            current_status_response.headers and \
            "Estamos+aguardando+novo+lote+de+vacina+para+abertura+de+novas+vagas" in current_status_response.headers['Location']
        # True until the world change
        return (True, vaccines_only_for_entrepreneurs, current_status_response.status_code)
    except Exception as e:
        log.error(f"Rolling, turning, diving, going in again {e}")
        return (True, False, 666)

def main():
    log.info("We need to stay alive until the last fucking politician dies! Up the Irons")
    while True:
        (kill_now, vaccines_only_for_entrepreneurs, status_code) = do_i_need_to_kill_the_president()
        log.info(f"vaccines_only_for_entrepreneurs? {vaccines_only_for_entrepreneurs} :: {status_code}")
        if not vaccines_only_for_entrepreneurs:
            send_message(f"{status_code} será? https://pronto.blumenau.sc.gov.br/pronto/agendamentovacinacaointerno.aspx")
            time.sleep(wait_when_change_minutes * 60)
        time.sleep(2.5)

if __name__ == "__main__":
    main()
