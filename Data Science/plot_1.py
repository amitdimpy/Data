import numpy as np
import matplotlib.pyplot as plt

a = ['06-Nov','05-Nov','04-Nov','03-Nov','02-Nov','01-Nov','31-Oct']
EWS = [65792,69975,77748,69493,62284,64823,69828]
FT = [39218,57631,47372,47375,48372,52885,55911]
FDC = [1267117,1268541,1265570,1267762,1316507,1709767,1814031]
KLARF = [146772,145852,141579,137455,136816,145901,151976]

x = np.arange(len(a))
width = 0.2

fig, ax = plt.subplots(figsize=(10,6))

rects1 = ax.bar(x - 1.5*width, EWS, width, label='EWS', color='r')
rects2 = ax.bar(x - 0.5*width, FT, width, label='FT', color='b')
rects3 = ax.bar(x + 0.5*width, FDC, width, label='FDC', color='g')
rects4 = ax.bar(x + 1.5*width, KLARF, width, label='KLARF', color='c')

ax.set_xlabel('Date')
ax.set_ylabel('File Count')
ax.set_title('Azure Copy Report')
ax.set_xticks(x)
ax.set_xticklabels(a)
plt.xticks(rotation=45)
ax.legend()

def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:,}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

add_labels(rects1)
add_labels(rects2)
add_labels(rects3)
add_labels(rects4)

plt.tight_layout()
plt.savefig('azure_copy_report.png', dpi=300, bbox_inches='tight')
plt.show()