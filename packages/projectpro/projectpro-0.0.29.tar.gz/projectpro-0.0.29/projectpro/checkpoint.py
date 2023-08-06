import projectpro.utils as utils
import signal
import time
import os,sys
import requests

global flag
flag=0

def run_with_timeout(func, args=(), kwargs={}, timeout_duration=2, default="Nope"):
    # Define a decorator that sets a timer limit for the function

    # Define a function to run the decorated function and handle timeouts
    def func_wrapper():
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            result = default
        return result

    # Start a timer to limit the execution time of the function
    start_time = time.time()
    result = "Nope"
    while True:
        result = func_wrapper()
        if result != "Nope":
            break
        elif time.time() - start_time > timeout_duration:
            
            break

    return result

def handler(signum, frame):
    global flag
    flag=1
    #os._exit(0)
    raise Exception("Time's up!")
    #raise Exception("Time's up!")


def checkpoint(puid=""):
    is_colab=False
    is_jupyter_notebook=False
    is_PY=False
    log_data=dict()
    log_data['puid']=str(puid)
    log_data['ip']="None"
    os_flag=False
    global flag

    if sys.platform!='win32':
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(10) # set timer for 10 seconds
    else:
        os_flag=True
        flag=1
    
    # signal.signal(signal.SIGALRM, handler)
    # signal.setitimer(signal.ITIMER_REAL, 2)

    
    try:
        
        if os_flag==True:
            raise Exception("Windows OS")
        
        if(utils.check_internet()==False):
            return

        if(utils.in_colab()):
            is_colab=True
            log_data['is_colab']=True
            log_data={**log_data, **utils.ipynb_name_colab()} 
            log_data={**log_data, **utils.get_ip_colab()}
            log_data={**log_data, **utils.get_exec_machine()}

            cells_index=utils.get_colab_cell()
            if(cells_index!=None):
                exec_details=utils.get_colab_cell_source(cells_index[0],cells_index[1]-1)
                log_data={**log_data, **exec_details}
            response=utils.push_log(log_data)
            return
        
        
        elif(utils.py_path()!=None):
            is_PY=True
            log_data['file_name']=utils.py_path()

            log_data={**log_data, **utils.get_exec_machine()}
        
            log_data={**log_data, **utils.get_py_line()}
            

            ip_script=utils.get_ip_script()
            
            log_data={**log_data, **utils.get_loc(ip_script)}
            
            if("None" not in log_data['ip']):
                response=utils.push_log(log_data)
            return

        elif(utils.in_notebook()):
            is_jupyter_notebook=True
            log_data['is_jupyter_notebook']=True

            log_data={**log_data, **utils.get_notebook_name()}
            ip=utils.get_ip_script()
            log_data={**log_data, **utils.get_loc(ip)}
            log_data={**log_data, **utils.get_exec_machine()}
            utils.push_log(log_data)

            utils.get_ip_jupyter()
            return

        else:
            return
    except Exception as e:
        return
       
    finally:
        if os_flag==False:
            signal.alarm(0) 
        if(flag==1):
                if os_flag==False:
                    signal.signal(signal.SIGALRM, handler)
                    signal.alarm(3) # set timer for 5 seconds
                try:
                    log_data=dict()
                    log_data['puid']=str(puid)
                    
                    ip_Ad = requests.get('https://checkip.amazonaws.com').text.strip()
                    log_data={**log_data, **utils.get_loc(ip_Ad)}
                    log_data['ip_flag']="Time up, AWS IP API"
                    log_data={**log_data, **utils.get_exec_machine()}
                    
                    if(utils.py_path()!=None):
                        log_data['file_name']=utils.py_path()
                        log_data={**log_data, **utils.get_py_line()}
                    elif(utils.in_colab()):
                        is_colab=True
                        log_data['is_colab']=is_colab
                        log_data={**log_data, **utils.ipynb_name_colab()} 
                    elif(utils.in_notebook()):
                        is_jupyter_notebook=True
                        log_data['is_jupyter_notebook']=is_jupyter_notebook
                        log_data={**log_data, **utils.get_notebook_name()}
                    utils.push_log(log_data)

                except:
                    pass
                finally:
                    if os_flag==False: 
                        signal.alarm(0) 
                    return
        else:
            return

def preserve(puid=""):
    checkpoint(puid)

def image_processing(puid=""):
    checkpoint(puid)

def decomposition(puid=""):
    checkpoint(puid)

def save_point(puid=""):
    checkpoint(puid)

def neural_layers(puid=""):
    checkpoint(puid)

def data_pipeline(puid=""):
    checkpoint(puid)

def loss_functions(puid=""):
    checkpoint(puid)

def recurrent_layers(puid=""):
    checkpoint(puid)

def model_snapshot(puid=""):
    checkpoint(puid)

def tensor_convert(puid=""):
    checkpoint(puid)

def mo_distance(puid=""):
    checkpoint(puid)

def feedback():
    from IPython.display import HTML
    return HTML('''
    <iframe 
	    src="https://docs.google.com/forms/d/e/1FAIpQLScs70rjp77cH8TmVpH7jFhas7dmlCWSKEnNJnooa8meVUSnZA/viewform?usp=sf_link" 
	    width="100%" 
	    height="1200px" 
	    frameborder="0" 
	    marginheight="0" 
	    marginwidth="0">
	    Loading...
    </iframe>
    ''')

#https://docs.google.com/forms/d/e/1FAIpQLScs70rjp77cH8TmVpH7jFhas7dmlCWSKEnNJnooa8meVUSnZA/viewform?usp=sf_link


def show_video(id):
    from IPython.display import HTML
    
    script = """
        <div align="center">
        <iframe width="100%" height="500"
        src="https://youtube.com/embed/{0}"
        </iframe>
        </div>
    """.format(id)
    
    return HTML(script)




      
            

        













        













#     js_query='''
#     function reqListener () {

#     var ipResponse = this.responseText
#     console.log(ipResponse);
#     //return ipResponse

#     const req2 = new XMLHttpRequest();
#     req2.addEventListener("load",function(){

#         //  this blocks runs after req2 and prints whole data    
#     console.log(this.responseText)
#     //document.querySelector("#output-area").appendChild(document.createTextNode(JSON.stringify(this.responseText)));

#     var command= "json_obj = " + JSON.stringify(this.responseText)
#    var kernel = IPython.notebook.kernel;
#    kernel.execute(command);
#     return JSON.stringify(this.responseText)


#     });
#     req2.open("GET", "https://ipapi.co/"+JSON.parse(ipResponse).ip+"/json/");
#     req2.send();


#     }

#     const req = new XMLHttpRequest();
#     req.addEventListener("load", reqListener);
#     req.open("GET", "https://api64.ipify.org?format=json");
#     req.send();
#     '''

#     p=IPython.display.Javascript(js_query)
#     return p
