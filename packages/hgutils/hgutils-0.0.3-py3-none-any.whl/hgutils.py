import time
from datetime import timedelta, datetime

def daterange(start_date, end_date, inclusive=True):
    if inclusive:
        included_dates = 1
    else:
        included_dates = 0
    for n in range(int((end_date-start_date).days+included_dates)):
        yield start_date + timedelta(n)

def to_currency (value, multiplier=100, add_currency_symbol=True, currency_symbol = '₹',rounding=0):
    negative_sign = ""
    if value < 0:
        negative_sign = "-"
        value = abs(value)
    value = round(value,rounding)
    decimal_value = round(value%1,rounding)
    value = int(round((value-decimal_value),0))
    if decimal_value == 0:
        currency_string = "" 
    else:
        currency_string = "." + str(decimal_value)[2:]
    base = 1_000
    set = value%base
    currency_string = str(int(round(set,0))) + currency_string
    if (len(str(set)) < len(str(value))) & (len(str(set)) < len(str(base))-1):
        zeros = "".join(['0' for _ in range(len(str(base))-1-len(str(set)))])
        currency_string = zeros + currency_string
        
    converted_value = set
    if set == value:
        if add_currency_symbol:
            return (currency_symbol + " " + negative_sign + currency_string).strip()
        else: 
            return (negative_sign + currency_string).strip()
    else:
        while converted_value != value:
            base = base * multiplier
            set = int(round((value%base - converted_value)/base * multiplier,0))
            currency_string = str(int(set)) + "," + currency_string
            if (len(str(int(round(set*base/multiplier,0)))) < len(str(value))) & (len(str(set)) < len(str(multiplier))-1):
                zeros = "".join(['0' for _ in range(len(str(multiplier))-1-len(str(set)))])
                currency_string = zeros + currency_string
            converted_value = int(round(converted_value + (set*base/multiplier),0))

    if add_currency_symbol:
        return (currency_symbol + " " + negative_sign + currency_string).strip()
    else: 
        return (negative_sign + currency_string).strip
    

class timer ():
    def __init__(self,name=None) -> None:
        self.stopwatches = {'name':name,'start_time':time.time(),
                    'stop_time':None,'parent':None,'children':[],
                    'depth':0}
        self.current_stopwatch = self.stopwatches
    
    def reset(self) -> None:

        del self.stopwatches
        self.__init__()

    def start(self,name=None) -> None:
        stopwatch = {'name':name,'start_time':time.time(),'stop_time':None,
                'parent':self.current_stopwatch,'children':[],
                'depth':self.current_stopwatch['depth']+1}
        self.current_stopwatch['children'].append(stopwatch)
        self.current_stopwatch = self.current_stopwatch['children'][-1]

    def stop(self,print=False,units='auto',verbose=0) -> None:
        self.current_stopwatch['stop_time'] = time.time()
        if print:
            self.print(units=units,verbose=verbose)
        self.current_stopwatch = self.current_stopwatch['parent']

    def _print_stopwatch(self,stopwatch,units):
            batting = ""
            if stopwatch['stop_time'] is None:
                t = time.time() - stopwatch['start_time']
                batting = "*"
            else:
                t = stopwatch['stop_time'] - stopwatch['start_time']
            if units == 'seconds':
                t = round(t,2)
            elif units == 'milliseconds':
                t = round(t*1000,2)
            elif units == 'minutes':
                t = round(t/60,2)
            elif units == 'hours':
                t = round(t/3_600,2)
            elif units == 'days':
                t = round(t/86_400,2)
            elif units == 'auto':
                if t <= .1:
                    t = round(t*1000,2)
                    units = 'milliseconds'
                elif t < 60:
                    t = round(t,2)
                    units = 'seconds'
                elif t > 60:
                    t = round(t/60,2)
                    units = 'minutes'
                elif t > 3_600:
                    t = round(t/3_600,2)
                    units = 'hours'
                elif t > 86_400:
                    t = round(t/86_400,2)
                    units = 'days'
            
            print("\t"*stopwatch['depth'],f'''{stopwatch['name']} - {t} {units}{batting}''')

    def _print_stopwatch_and_children(self,stopwatch,units):
        self._print_stopwatch(stopwatch,units=units)
        for children_stopwatch in stopwatch['children']:
            self._print_stopwatch_and_children(children_stopwatch,units=units)

    def print(self,units='auto',verbose=0):
        
        if verbose==0:
            self._print_stopwatch(self.current_stopwatch,units=units)
        elif verbose==1:
            self._print_stopwatch(self.current_stopwatch['parent'],units=units)
            self._print_stopwatch(self.current_stopwatch,units=units)
        elif verbose==2:
            self._print_stopwatch_and_children(self.stopwatches,units=units)


class debugger():
    '''
    debugger class
    functionality:
    execute: print and/or execute set of statements
        while in debugger mode.
        Do nothing otherwise.
    '''
    def __init__(self,name=None,is_debugging = False) -> None:
        self.name = 'debugger'
        if name:
            self.name=name
        self._is_debugging = is_debugging

    def set_debugging_status(self,debugging_status=False):
        '''
        Set debugging status as per received argument
        '''
        self._is_debugging = debugging_status

    def debugging_on(self):
        '''
        Set debugging to ON
        '''
        self.set_debugging_status(True)

    def debugging_off(self):
        '''
        Set debugging to OFF
        '''
        self.set_debugging_status(False)

    def execute(self,print_signature=False,
                print_name=False,
                print_timestamp=False,
                **kwargs):
        '''
        print and/or execute set of command(s) when in debugger mode.
        Do nothing otherwise.
        title: title of current execution
        print: argument to be printed
        execute: function to be executed
        args: arguments to functions to be executed
        print_signature: print name of debugger and timestamp
        '''
        if self._is_debugging:
            if 'title' in kwargs:
                print(f'''{kwargs['title']}:''')
            if 'print' in kwargs:
                print(kwargs['print'])
            if 'execute' in kwargs:
                if 'args' in kwargs:
                    if (type(kwargs['args']) is list) or (type(kwargs['args']) is tuple):
                        kwargs['execute'](*kwargs['args'])
                    else:
                        kwargs['execute'](kwargs['args'])
                else:
                    kwargs['execute']()
            if print_name:
                print("By:\t", self.name)

            if print_timestamp:
                print("@:\t",datetime.now())
                print("Getting printed")

            if print_signature:
                print("By:\t", self.name)
                print("@:\t",datetime.now())


if __name__ == '__main__':
    print("Yes")
    t = timer("Testing timer")
    time.sleep(2)
    t.start("Exterior")
    for i in range(4):
        t.start("i="+str(i))
        time.sleep(1)    
        if i==2:
            for j in range(5):
                t.start("j="+str(j))
                time.sleep(.04)
                t.stop(print=True,verbose=1)
        t.stop(print=True,verbose=1)
    t.stop(print=True,verbose=1)
    # t.print(verbose=2)


