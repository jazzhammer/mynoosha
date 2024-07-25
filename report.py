from mynoosha import mynoosha_greeting
from test_integration import test_clients_ping

def report_mynoosha():
    print(f"reporting on mynoosha from mynoosha root !!")
    mynoosha_greeting()
    test_clients_ping()

if __name__=="__main__":
    report_mynoosha()
