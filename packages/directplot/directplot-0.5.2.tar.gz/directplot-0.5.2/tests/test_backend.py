import matplotlib.pyplot as _plt

__version__ = '0.5.2'

def onImport():
    handleBackend()
    print()

def handleBackend():
    initialBackend = _plt.get_backend()
    targetBackends = ['TkAgg', 'GTK3Agg'] # Currently best for Windows, MacOS and Linux
    targetBackendsLower = [tbe.lower() for tbe in targetBackends]

    print(f'directplot v{__version__} with backend {initialBackend}', end='', flush=True)

    # Test if we have one of the target backends:
    if initialBackend.lower() in targetBackendsLower:
        # Yes. All fine. Just end current line with a new line
        print('', flush=True)
    else:
        # No. Let's try to switch to one of the targetBackends:
        for targetBackend in targetBackends:
            print(f' > {targetBackend}', end='', flush=True)
            try:
                _plt.switch_backend(targetBackend)
            except Exception as exceptionDetails:
                # Switch did not succeed:
                print(f' ({exceptionDetails}) > {_plt.get_backend()}', end='', flush=True)
            else:
                # Switch succeeded, we are done.
                break
        # End current line with a new line.
        print('', flush=True)

onImport()
print('=== FERTIG ===')
