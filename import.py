from core import configurator, importer
import xlsxwriter

config = configurator.load_config()

sources = []
pairs = []
for source in config['source']:
    fromData = importer.import_tree(source['from'], source['mask'])
    toData = importer.import_tree(source['to'], source['mask'])
    pairs.append({'from': fromData, 'to': toData, 'main': source['main']})
    sources.append(fromData)
    sources.append(toData)

target = importer.import_tree(config['target']['dir'], config['target']['mask'])

diffs = []
for pair in pairs:
    if pair['main']:
        fromData = pair['from']
        toData = pair['to']
        for key, val in toData.items():
            if key in fromData:
                old = fromData[key]
                if val != old:
                    print("-> {} = {} -> {}".format(key, old, val))
                    diffs.append(key)
            else:
                print("++ {} = {}".format(key, val))
        for key, old in fromData.items():
            if key not in toData:
                print("-- {} = {}".format(key, old))
print("{} strings changed".format(len(diffs)))

print("Generating output {}".format(config['output']['file']))
workbook = xlsxwriter.Workbook(config['output']['file'])
sheet1 = workbook.add_worksheet()

# headers
col = 1
sheet1.write(0, 0, "key")
sheet1.set_column(0, 0, 50)
for source in sources:
    sheet1.set_column(col, col, 100)
    col += 1
sheet1.set_column(col, col, 100)

# data
row = 1
for key in diffs:
    sheet1.write_string(row, 0, key)
    col = 1
    for source in sources:
        if key in source:
            sheet1.write_string(row, col, source[key])
        else:
            sheet1.write_string(row, col, "")
        col += 1
    if key in target:
        sheet1.write_string(row, col, target[key])
    else:
        sheet1.write_string(row, col, "")
    row += 1

workbook.close()
