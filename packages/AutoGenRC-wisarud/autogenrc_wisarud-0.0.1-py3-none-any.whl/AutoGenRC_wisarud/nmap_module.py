import nmap3
import json
import base
import datetime
import validate


def nmap_scan():
    nmap = nmap3.Nmap()
    date = datetime.datetime.now()
    ip_address = base.settings['target_ip']
    version_result = ''
    while True:
        try:
            if(validate.validate_ip_address(ip_address)): 
                # ip_address = base.settings['target_ip']
                print('Scanning for ip = '+ip_address)
                version_result = nmap.nmap_version_detection(base.settings['target_ip']) 
                json_formatted_str = json.dumps(version_result, indent=4,sort_keys=True)
                jj = json.loads(json_formatted_str)
                data = jj['192.168.184.129']['ports']
                with open(base.NMAP_REPORT_PATH+ ip_address + '_'+ str(date.date()) +'.txt', 'w') as f:
                    f.write("IP: %s\n" % ip_address)
                    print("IP: %s" % ip_address)
                    for port in data:
                        # 4 case 
                        # have all information
                        # print(port)
                        base.open_port.append(port['portid'])
                        if(port['state'] == 'open' and 'version' in port['service'].keys() and 'product' in port['service'].keys()):
                            print('PORT: ' +port['portid']+'/'+port['protocol'] +' SERVICE: '+port['service']['name'] + ' VERSION: ' + port['service']['product'] + ' ' + port['service']['version'])
                            f.write('PORT: ' +port['portid']+'/'+port['protocol'] +' SERVICE: '+port['service']['name'] + ' VERSION: ' + port['service']['product'] + ' ' + port['service']['version'])
                            f.write('\n')
                        elif(port['state'] == 'open' and 'version' in port['service'].keys()): # have only version keys
                            # print('Im only have version key!!')
                            print('PORT: ' +port['portid']+'/'+port['protocol']+' SERVICE: '+port['service']['name']+ ' VERSION: ' + port['service']['version'])
                            f.write('PORT: ' +port['portid']+'/'+port['protocol']+' SERVICE: '+port['service']['name']+ ' VERSION: ' + port['service']['version'])
                            f.write('\n')
                        elif(port['state'] == 'open' and 'product' in port['service'].keys()): # have only product keys 
                            # print('Im only have product key!!')
                            print('PORT: ' +port['portid']+'/'+port['protocol']+' SERVICE: '+port['service']['name']+ ' VERSION: ' + port['service']['product'])
                            f.write('PORT: ' +port['portid']+'/'+port['protocol']+' SERVICE: '+port['service']['name']+ ' VERSION: ' + port['service']['product'])
                            f.write('\n')
                        elif(port['state'] == 'open'): # dont have version and product keys
                            # print('Im dont have both extras keys!!')
                            print('PORT: ' +port['portid']+'/'+port['protocol']+' SERVICE: '+port['service']['name'] + ' VERSION: ')
                            f.write('PORT: ' +port['portid']+'/'+port['protocol']+' SERVICE: '+port['service']['name'] + ' VERSION: ')
                            f.write('\n')
                            
                    break 
            else:
                print('Error: Invalid Ip address')
                break
                
        except KeyboardInterrupt:
            break
        except :
            print('Error: Please try again')
            break


    
    

def main():
    print('nmap module')
# This line runs the main function
if __name__ == "__main__":
    main()