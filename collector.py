import time
import psutil
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "my-super-secret-token" 
INFLUXDB_ORG = "my-org"                
INFLUXDB_BUCKET = "my-bucket"             


def main():
    print("Connecting to InfluxDB...")
    try:
 
        client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        
 
        write_api = client.write_api(write_options=SYNCHRONOUS)
        print("Connection successful. Starting data collection...")
        
    except Exception as e:
        print(f"Could not connect to InfluxDB: {e}")
        return

  
    while True:
        try:
            
            
            # interval=None gets the usage since the last call (or system boot)
            cpu_percent = psutil.cpu_percent(interval=None) 
            mem_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent
            
    
            
      
            p_cpu = Point("system_metrics").field("cpu_percent", float(cpu_percent))
            p_mem = Point("system_metrics").field("mem_percent", float(mem_percent))
            p_disk = Point("system_metrics").field("disk_percent", float(disk_percent))

          
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=[p_cpu, p_mem, p_disk])
            
            
            print(f"Data written: CPU {cpu_percent}%, MEM {mem_percent}%, DISK {disk_percent}%")

         
            time.sleep(5)
            
        except KeyboardInterrupt:
           
            print("\nStopping collector.")
            break
        except Exception as e:
     
            print(f"An error occurred: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()