# 🖨 Python CUPS print options generator from PPD

## 📥 Installation

### 📦 From pip:

```shell
python -m pip install -U pycups_po
```

### 🏗 From git:

```shell
git clone https://github.com/WhiteApfel/pycups_po.git
cd pycups_po
python setup.py install
```


## 🧑‍🏫 How to use

### 🐍 Example

```python
import cups

from pycups_po import PrinterOptionsGenerator
from pycups_po.models import PrinterOption

conn = cups.Connection()

generator = PrinterOptionsGenerator(conn, "CT-S2000")

ops: list[PrinterOption] = generator.get_ppd_options()
for op in ops:
    print(op)

with open("tr4500.py", "w+") as f:
    f.write(generator.generate_options_dataclass(printer_name="TR-4500"))
```

You can specify name of printer when init `PrinterOptionsGenerator`, then it will be used by default. 
Or you can pass name to function.

### 📋 Dataclasses
```python
@dataclass
class OptionValue:
    value: str
    pretty_value: str
    content: str


@dataclass
class PrinterOption:
    name: str
    pretty_name: Optional[str]
    type: Literal["PickOne"]
    default_value: str
    values: List[OptionValue]
```

### 💻 CLI

**Show list of printers**
```shell
pycups_po printers
# or
pycups_po printers --host 192.168.1.12
# or 
pycups_po printers --host 192.168.1.12 --port 6631
```

```
🖨 Printers
├── CT-S2000
│   ├── Info: CITIZEN CT-S2000
│   └── State: ⏳ idle
└── TR4540
    ├── Info: Canon TR4540
    └── State: ⏳ idle

```

**Show options**
```shell
pycups_po options TR4540
# You can set the --host and --port in the same way
```

```
⚙️ Options
├── MediaType (Media Type)
│   ├── Type: PickOne
│   ├── Default: matte
│   └── Values:
│       ├── 'plain' (Plain Paper): <</MediaType(plain)>>setpagedevice
│       ├── 'glossygold' (Photo Paper Plus Glossy II): <</MediaType(glossygold)>>setpagedevice
...
├── Duplex (Duplex Printing)
│   ├── Type: PickOne
│   ├── Default: None
│   └── Values:
│       ├── 'None' (Off): 
│       ├── 'DuplexNoTumble' (Long-side stapling): 
│       └── 'DuplexTumble' (Short-side stapling): 
└── ColorModel (Color Model)
    ├── Type: PickOne
    ├── Default: rgb
    └── Values:
        └── 'rgb' (RGB): 
```

**Generate dataclass file**
```shell
pycups_po generate -o ./tr4540.py TR4540
# or
pycups_po generate --output-file ~/printer.py TR4540
# You can set the --host and --port in the same way
```