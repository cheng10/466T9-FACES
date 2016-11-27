import csv, collections

res = {'0397_3': 0.12034804, '0424_1': 0.8592248, '0299_3': 0.038445193, '0424_3': 0.13216113, '0424_2': 0.07866744, '0424_4': 0.50070906}
writer_res = {}

for i in range(283, 476):
    writer_res[i] = 0
print writer_res

for key, value in res.iteritems():
    writer_res[int(key[1:4])] += value
print writer_res 

ordered_res = collections.OrderedDict(sorted(writer_res.items()))
print ordered_res

for key, value in ordered_res.items():
    ordered_res[key] = value / 4

with open('res.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for key,value in ordered_res.iteritems():
        spamwriter.writerow([key, value])