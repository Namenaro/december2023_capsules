import base64
import os.path
from io import BytesIO
import matplotlib.pyplot as plt
from pandas import DataFrame
import numpy as np

class HtmlLogger:
    def __init__(self, name, dir_path=None):
        self.name = name
        self.html = ''
        self.dir_path = dir_path

    def add_line_little(self):
        self.html += "<hr>"
        self.save()

    def add_line_big(self):
        self.html += "<hr style=\"height:10px;background:gray\">"
        self.save()

    def add_text(self, text):
        self.html += text + '<br>'
        self.save()

    def add_fig(self, fig):
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png', pad_inches=0.0, bbox_inches="tight")
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        self.html += '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + '<br>'
        plt.close(fig)
        self.save()

    def save(self):
        filename = self.name + '.html'
        if self.dir_path is not None:
            filename = os.path.join(self.dir_path, filename)
        with open(filename, 'w') as f:
            f.write(self.html)

    def add_dataframe(self, df):
        table = df.to_html(index=False, classes='table table-striped', border="0", float_format="{:,.2f}".format)
        styled_table = table.replace('<th>', '<th style = "background-color: #b11a21; padding: 10px; color: #ffe8e8;">')
        styled_table = styled_table.replace('<tr>',
                                     '<tr style = "background-color: #ebebeb; color: #e0474c;">')
        self.add_text(styled_table)


if __name__ == '__main__':
    def draw_smth():
        fig, ax = plt.subplots()
        ax.plot([1,2,3,4,3,2,1])
        return fig

    log = HtmlLogger("my_log")

    fig = draw_smth()
    log.add_fig(fig)

    log.add_text("hjhkjdfgkjgkjh")

    fig = draw_smth()
    log.add_fig(fig)

    log.add_line_little()
    log.add_text("1111111")

    df = DataFrame({'foo1': np.random.randn(2),
                    'foo2': np.random.randn(2)})

    log.add_dataframe(df)
