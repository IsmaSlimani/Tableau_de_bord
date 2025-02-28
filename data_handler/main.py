import subprocess

from data_handler.genarate_sessions import generate_sessions
from data_handler.generate_levels_metrics import generate_levels_metrics
from data_handler.generate_data_processed import generate_data_processed
from data_handler.generate_players_processed import generate_players_processed


def run_js_script(node_file):
    try:
        result = subprocess.run(
            ["node", node_file],  
            text=True,            
            capture_output=True,  
            check=True            
        )
        print("Node.js Output:")
        print(result.stdout)   
    except subprocess.CalledProcessError as e:
        print("Error running Node.js file:")
        print(e.stderr) 

def data_handler():
    run_js_script("./data_handler/main.js")
    generate_data_processed()
    generate_levels_metrics()
    generate_players_processed()
    generate_sessions()