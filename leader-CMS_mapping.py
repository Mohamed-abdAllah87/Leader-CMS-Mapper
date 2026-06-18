import queue
import requests
import threading
import sys

THREADS = 20
TARGET = input("[*] Enter your target link : ").strip().rstrip('/')
WORDLIST = input("[*] Enter your word list path : ").strip()
OUTPUT_FILE = input("[*] Enter output report name (e.g., report.txt) : ").strip()

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"

results_queue = queue.Queue()

def build_wordlist(wordlist_file):
    words = queue.Queue()
    try:
        with open(wordlist_file, "r") as f:
            raw_words = f.read().splitlines()

        for word in raw_words:
            if not word.startswith("/"):
                word = f"/{word}"
            words.put(word)

        return words
    
    except FileNotFoundError:
        print(f"[-] Error: Wordlist file '{wordlist_file}' not found!")
        sys.exit()

def test_remote(word_queue):
    headers = {'user-Agent': USER_AGENT}
    while not word_queue.empty():
        try:
            url_path = word_queue.get(block=False)
            full_url = f"{TARGET}{url_path}"
            response = requests.get(full_url, headers=headers, timeout=5)

            if response.status_code == 200:
                result_text = f"[+] Found (200 OK): {full_url}"
                print(result_text)
                results_queue.put(result_text) 
                
            elif response.status_code == 403:
                result_text = f"[!] Restricted (403 Forbidden): {full_url} -> (Target folder exists!)"
                print(result_text)
                results_queue.put(result_text) 
            
            else:
                print(f"[-] Checking: {url_path} ...", end="\r")
                
            word_queue.task_done()
        except queue.Empty:
            break
        except requests.exceptions.RequestException:
            if 'url_path' in locals():
                word_queue.task_done()
            continue

if __name__ == "__main__":
    print("\n[*] Threaded CMS Mapper Started...")
    print(f"[*] Target Site: {TARGET}")
    print(f"[*] Spawning {THREADS} attacking threads...")

    word_queue = build_wordlist(WORDLIST)
    print(f"[+] Queue loaded with {word_queue.qsize()} paths.")
    print("[*] Hunting for hidden installation files and directories...\n")

    threads_list = []
    for i in range(THREADS):
        t = threading.Thread(target=test_remote, args=(word_queue,))
        threads_list.append(t)
        t.start()
        
    for t in threads_list:
        t.join()
        
    print("\n\n[+] Done! Mapping operation completed. Writing report...")

    if not results_queue.empty():
        try:
            with open(OUTPUT_FILE, "w") as report:
                report.write(f"=== CMS Mapping Report for {TARGET} ===\n")
                report.write(f"[*] Total valid paths found: {results_queue.qsize()}\n")
                report.write("==================================================\n\n")
                
                while not results_queue.empty():
                    report.write(results_queue.get() + "\n")
                    
            print(f"[+] Report saved successfully to: {OUTPUT_FILE} 📄")
        except Exception as e:
            print(f"[-] Error writing to file: {e}")
    else:
        print("[-] No valid paths were found. No report file generated.")


    print("[*] All targets checked. Leader-CMS-Mapper shutting down. 🫡")
