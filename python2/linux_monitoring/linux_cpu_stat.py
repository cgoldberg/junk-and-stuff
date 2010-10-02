#!/usr/bin/env python
#  Corey Goldberg - 2010
#  linux_cpu_stat


"""
    linux_cpu_stat - Python Module for CPU Stats on Linux
    
    requires:
    - Python 2.6+
    - Linux 2.6.x
    
    
    functions:
    - cpu_percents(sample_duration=1)
    - cpu_times()
    - procs_running()
    - procs_blocked()
    - load_avg()
    - cpu_info()
    
    
    simple example:
    
        #!/usr/bin/env python
        import linux_cpu_stat as cpustat
        print cpustat.cpu_info()
    
    
    full example:
    
        #!/usr/bin/env python
        
        import linux_cpu_stat as cpustat   

        cpu_pcts = cpustat.cpu_percents()

        print 'cpu utilization: %.2f%%' % (100 - cpu_pcts['idle']) 
        
        print 'cpu mode percents:'
        pprint.pprint(cpu_pcts)

        print 'cpu times:', cpustat.cpu_times()
        
        cpu_info = cpustat.cpu_info()
        
        print 'cpu info:'
        pprint.pprint(cpu_info)
        
        print 'num cores: %s' % cpu_info['cpu cores']
        
        print 'procs running: %d' % cpustat.procs_running()
        
        print 'procs blocked: %d' % cpustat.procs_blocked()    
        
        print 'load_avg:', cpustat.load_avg()
    
"""


import time



def cpu_times():
    """Return a sequence of cpu times.

    each number in the sequence is the amount of time, measured in units 
    of USER_HZ (1/100ths of a second on most architectures), that the system
    spent in each cpu mode: (user, nice, system, idle, iowait, irq, softirq, [steal], [guest]).
    
    on SMP systems, these are aggregates of all processors/cores.
    """
    
    with open('/proc/stat') as f:
        line = f.readline()
    
    cpu_times = [int(x) for x in line.split()[1:]]
    
    return cpu_times
    
    
    
def cpu_percents(sample_duration=1):
    """Return a dictionary of usage percentages and cpu modes.
    
    elapsed cpu time samples taken at 'sample_time (seconds)' apart.
    
    cpu modes: 'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq'
    
    on SMP systems, these are aggregates of all processors/cores.
    """
    
    deltas = __cpu_time_deltas(sample_duration)
    total = sum(deltas)
    percents = [100 - (100 * (float(total - x) / total)) for x in deltas]

    return {
        'user': percents[0],
        'nice': percents[1],
        'system': percents[2],
        'idle': percents[3],
        'iowait': percents[4],
        'irq': percents[5],
        'softirq': percents[6],
    }



def procs_running():
    """Return number of processes in runnable state."""
    
    return __proc_stat('procs_running')



def procs_blocked():
    """Return number of processes blocked waiting for I/O to complete."""
    
    return __proc_stat('procs_blocked')
    


def load_avg():
    """Return a sequence of system load averages (1min, 5min, 15min).
    
    number of jobs in the run queue or waiting for disk I/O 
    averaged over 1, 5, and 15 minutes
    """
    
    with open('/proc/loadavg') as f:
        line = f.readline()
    
    load_avgs = [float(x) for x in line.split()[:3]]
    
    return load_avgs
        


def cpu_info():
    """
    """
    
    with open('/proc/cpuinfo') as f:
        cpuinfo = {}
        for line in f:
            if ':' in line:
                fields = line.replace('\t', '').strip().split(': ')
                if fields[0] not in ('processor', 'core id'):  # core specific items
                    try:
                        cpuinfo[fields[0]] = fields[1]
                    except IndexError:
                        pass
        return cpuinfo



def __cpu_time_deltas(sample_duration):
    """Return a sequence of cpu time deltas for a sample period.
    
    elapsed cpu time samples taken at 'sample_time (seconds)' apart.
    
    each value in the sequence is the amount of time, measured in units 
    of USER_HZ (1/100ths of a second on most architectures), that the system
    spent in each cpu mode: (user, nice, system, idle, iowait, irq, softirq, [steal], [guest]).
    
    on SMP systems, these are aggregates of all processors/cores.
    """
    
    with open('/proc/stat') as f1:
        with open('/proc/stat') as f2:
            line1 = f1.readline()
            time.sleep(sample_duration)
            line2 = f2.readline()
    
    deltas = [int(b) - int(a) for a, b in zip(line1.split()[1:], line2.split()[1:])]
    
    return deltas
    
    
    
def __proc_stat(stat):
    with open('/proc/stat') as f:
        for line in f:
            if line.startswith(stat):
                return int(line.split()[1])
                
                



if __name__ == '__main__':   
    import pprint

    cpu_pcts = cpu_percents()

    print 'cpu utilization: %.2f%%' % (100 - cpu_pcts['idle']) 
    
    print 'cpu mode percents:'
    pprint.pprint(cpu_pcts)

    print 'cpu times:', cpu_times()
    
    cpu_info = cpu_info()
    
    print 'cpu info:'
    pprint.pprint(cpu_info)
    
    print 'num cores: %s' % cpu_info['cpu cores']
    
    print 'procs running: %d' % procs_running()
    
    print 'procs blocked: %d' % procs_blocked()    
    
    print 'load_avg:', load_avg()
    

