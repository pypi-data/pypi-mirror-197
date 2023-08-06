"""pandas utils"""

OHLC_OPT = dict(
    line_width=1,
    increasing_line_color="#00CC96",  # px.colors.qualitative.Plotly[2]
    decreasing_line_color="#FF6692",  # px.colors.qualitative.Plotly[6]
    tickwidth=0.3,
)

OHLCV_AGG_DICT = dict(
    open="first",
    high="max",
    low="min",
    close="last",
    volume="sum",
)


from dataclasses import dataclass


@dataclass
class multi_df_display:
    """HTML representation of multiple df, notebook only

    Args:
        dfs (dict[str, Dataframe]): {key: title, val: df}

    Examples:
        multi_df_display({
            'title 1': df1,
            'title 2': df2
        })
    """

    dfs: dict
    template = """
        <div style="float: left; padding: 10px;">
        <p style='font-family:"Courier New", Courier, monospace'>{0}</p>{1}
        </div>
    """

    def _repr_html_(self):
        """html representation"""
        htmls = [
            self.template.format(title, df._repr_html_())
            for title, df in self.dfs.items()
        ]
        return "\n".join(htmls)

    def __repr__(self):
        """string representation"""
        str_reps = [title + "\n" + repr(df) for title, df in self.dfs.items()]
        return "\n\n".join(str_reps)
