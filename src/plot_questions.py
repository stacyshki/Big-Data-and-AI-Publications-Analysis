import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from prettytable import PrettyTable


BG = "#0d1117"
FONT = "DM Mono, IBM Plex Mono, monospace"
FONT_MONO = "IBM Plex Mono, monospace"

_COLOR_TEAL = "#4ECDC4"
_COLOR_RED = "#FF6B6B"
_GRID = "rgba(255,255,255,0.06)"
_GRID2 = "#21262d"


def _print_block(title: str, content, width: int = 40) -> None:
    if isinstance(content, pd.DataFrame):
        df = content.copy()
        if not isinstance(df.index, pd.RangeIndex):
            df = df.reset_index()
            df.rename(columns={'index': 'metrics'}, inplace=True)
        pt = PrettyTable()
        pt.title = title
        pt.field_names = list(df.columns)
        for row in df.itertuples(index=False):
            pt.add_row(list(row))
        print(pt)
    elif isinstance(content, pd.Series):
        df = content.reset_index()
        df.columns = [content.index.name or "metrics", content.name or "value"]
        pt = PrettyTable()
        pt.title = title
        pt.field_names = list(df.columns)
        for row in df.itertuples(index=False):
            pt.add_row(list(row))
        print(pt)
    else:
        print("=" * width)
        print(f"  {title}")
        print("-" * width)
        print(content)
        print("=" * width)


def _base_layout(bg: str = BG, **overrides) -> dict:
    """Dark-theme base layout merged with caller overrides."""
    layout = dict(
        paper_bgcolor=bg,
        plot_bgcolor=bg,
        font=dict(color="#c9d1d9", family=FONT),
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(size=18, color="#e6edf3", family=FONT),
        ),
        margin=dict(t=80, b=40, l=40, r=40),
        height=450,
    )
    layout.update(overrides)
    return layout


def _axis(title: str = "", grid: bool = False, grid_color: str = _GRID,
          **kwargs) -> dict:
    """Convenience axis config builder."""
    return dict(
        title=title,
        showgrid=grid,
        gridcolor=grid_color if grid else None,
        zeroline=False,
        **kwargs,
    )


def _donut(df: pd.DataFrame, names: str, values: str, title: str,
            val_label: str = "Papers") -> go.Figure:
    """Styled donut / pie chart."""
    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.55,
        title=title,
        color_discrete_sequence=px.colors.sequential.Tealgrn,
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate=(
            f"<b>%{{label}}</b><br>{val_label}: %{{value}}"
            "<br>Share: %{percent}<extra></extra>"
        ),
        marker=dict(line=dict(color=BG, width=2)),
    )
    fig.update_layout(**_base_layout(
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    ))
    return fig


def _hbar(df: pd.DataFrame, x: str, y: str, title: str,
        x_title: str = "Number of Papers", margin_l: int = 120) -> go.Figure:
    """Styled horizontal bar chart with outside text labels."""
    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation="h",
        title=title,
        color=x,
        color_continuous_scale="Tealgrn",
    )
    fig.update_traces(
        text=df[x],
        textposition="outside",
        hovertemplate=f"<b>%{{y}}</b><br>{x_title}: %{{x}}<extra></extra>",
        marker=dict(line=dict(color=BG, width=1.5)),
    )
    fig.update_layout(**_base_layout(
        xaxis=_axis(x_title, grid=True),
        yaxis=_axis(),
        coloraxis_showscale=False,
        margin=dict(t=80, b=40, l=margin_l, r=40),
    ))
    fig.update_xaxes(range=[0, df[x].max() * 1.15])
    return fig


def _top10_other(df: pd.DataFrame, col: str = "papers") -> pd.DataFrame:
    """Return top-10 rows + aggregated 'Other' remainder, sorted descending."""
    df = df.sort_values(col, ascending=False).reset_index(drop=True)
    top = df.iloc[:10].copy()
    top.loc[len(top)] = ["Other", df.iloc[10:][col].sum()]
    return top.sort_values(col, ascending=False).reset_index(drop=True)


def _plot_venue_pair(df: pd.DataFrame, pie_title: str, bar_title: str,
                        bar_slice: slice = slice(None, 10),
                        margin_l: int = 120) -> None:
    """Donut + horizontal bar for a venue/papers DataFrame."""
    mp = _top10_other(df)
    _donut(mp, "venue", "papers", pie_title).show()

    bar_data = mp.sort_values("papers").iloc[bar_slice]
    _hbar(bar_data, "papers", "venue", bar_title, margin_l=margin_l).show()


def _evolution_hbar(df: pd.DataFrame, x: str, title: str,
                    x_title: str, range_x: list,
                    base: str | None, custom_label: str) -> go.Figure:
    """Horizontal bar used repeatedly in s7q1."""
    fig = px.bar(
        df,
        x=x,
        y="subtopic",
        orientation="h",
        base=base,
        color="totalVolume",
        range_x=range_x,
        title=title,
        custom_data=[x, "totalVolume"],
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            f"{custom_label}: %{{customdata[0]}}<br>"
            "Total volume: %{customdata[1]}<br>"
            "<extra></extra>"
        ),
        marker=dict(line=dict(color=BG, width=1)),
    )
    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family=FONT_MONO, color="#c9d1d9", size=12),
        xaxis=dict(title=x_title, gridcolor=_GRID2, linecolor="#30363d",
                    zeroline=False, tickcolor="#30363d"),
        yaxis=dict(title="Subtopic", gridcolor=_GRID2, linecolor="#30363d",
                    tickcolor="#30363d", autorange="reversed"),
        title=dict(x=0.04, font=dict(size=18, color="#e6edf3")),
        coloraxis_showscale=False,
        margin=dict(t=60, r=30, b=60, l=120),
    )
    return fig


def cumulate_vol_avg(
    df1: pd.DataFrame, df2: pd.DataFrame, df3: pd.DataFrame
) -> tuple[pd.Series, pd.Series]:
    """Weighted cumulative volume and average year across three DataFrames."""
    volumes = df1.totalVolume, df2.totalVolume, df3.totalVolume
    ttl_vol = sum(volumes)
    avg_year = sum(
        df.avgYear * (vol / ttl_vol)
        for df, vol in zip([df1, df2, df3], volumes)
    )
    return ttl_vol, avg_year


def s6q1(popular_articles: pd.DataFrame,
            popular_conferences: pd.DataFrame) -> None:
    _print_block("POPULAR ARTICLES", popular_articles.head(5), width=32)
    _print_block("ARTICLES ANALYSIS", popular_articles.describe(), width=20)
    _print_block("POPULAR CONFERENCES", popular_conferences.head(5), width=20)
    _print_block("CONFERENCES ANALYSIS", popular_conferences.describe(), 
                    width=20)

    _plot_venue_pair(
        popular_articles,
        pie_title="Top Publication Venues in Industry",
        bar_title="Top-10 Publication Venues",
        bar_slice=slice(0, 10),
    )
    _plot_venue_pair(
        popular_conferences,
        pie_title="Top Conferences in the Industry",
        bar_title="Top-10 Conferences",
        bar_slice=slice(0, 10),
        margin_l=140,
    )


def s6q2(ai_citations: pd.DataFrame) -> None:
    _print_block("OVERVIEW OF CATEGORIES", ai_citations, width=72)
    _print_block("CATEGORIES ANALYSIS", ai_citations.describe(), width=48)

    _donut(ai_citations, "category", "paperCount",
            "Paper Count per Category").show()
    _donut(ai_citations, "category", "totalCitations",
            "Citations per Category", val_label="Citations").show()

    fig = go.Figure(data=[
        go.Bar(
            name="Citations",
            x=ai_citations.category,
            y=ai_citations.totalCitations,
            marker=dict(color=_COLOR_RED, line=dict(color=BG, width=1.5)),
            hovertemplate="<b>%{x}</b><br>Citations: %{y}<extra></extra>",
        ),
        go.Bar(
            name="Papers",
            x=ai_citations.category,
            y=ai_citations.paperCount,
            marker=dict(color=_COLOR_TEAL, line=dict(color=BG, width=1.5)),
            hovertemplate="<b>%{x}</b><br>Papers: %{y}<extra></extra>",
        ),
    ])
    fig.update_layout(**_base_layout(
        barmode="group",
        xaxis=_axis(tickangle=-20),
        yaxis=_axis("Count", grid=True),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h",
                    y=1.08, x=0.5, xanchor="center"),
        margin=dict(t=90, b=80, l=60, r=40),
    ))
    fig.show()

    ai_citations["citPerPaper"] = (
        ai_citations.totalCitations / ai_citations.paperCount
    )

    fig = px.bar(
        ai_citations,
        x="category",
        y="citPerPaper",
        color="citPerPaper",
        title="Citations per Paper by Category",
        color_continuous_scale="Tealgrn",
    )
    fig.update_traces(
        text=ai_citations["citPerPaper"].round(2),
        textposition="outside",
        marker=dict(line=dict(color=BG, width=1.5)),
        hovertemplate="<b>%{x}</b><br>Citations per Paper: %{y:.2f}<extra></extra>",
    )
    fig.update_layout(**_base_layout(
        xaxis=_axis(tickangle=-20),
        yaxis=_axis("Citations per Paper", grid=True),
        coloraxis_showscale=False,
        margin=dict(t=60, b=80, l=60, r=40),
    ))
    fig.show()

    _print_block("CITATIONS PER PAPER ANALYSIS", 
                    ai_citations.citPerPaper.describe(), width=35)


def s7q1(
    df_before2011: pd.DataFrame,
    df_from2021onwards: pd.DataFrame,
    df_2011to2021: pd.DataFrame,
    funap_df: pd.DataFrame,
) -> None:
    for df in (df_before2011, df_from2021onwards, df_2011to2021):
        df.sort_values("subtopic", inplace=True, ignore_index=True)

    volume, average_year = cumulate_vol_avg(
        df_from2021onwards, df_before2011, df_2011to2021
    )

    evolution = df_before2011.iloc[:, :2].copy()
    evolution["avgYear"] = average_year
    evolution["totalVolume"] = volume

    _print_block("EVOLUTION OF TOPICS", evolution, width=65)
    _print_block("ANALYSIS OF EVOLUTION", evolution.describe(), width=47)

    dates = evolution.birthYear + np.array([0, 0, 0.7, 0, 0.7, 0, 0, 0])
    labels = evolution.subtopic
    x_stem = np.array([2.0 if i % 2 == 0 else -2.0 for i in range(len(dates))])
    x_label = x_stem.copy()

    for i, lbl in enumerate(labels):
        if lbl == "Ethics & Interpretability":
            x_label[i] = -2

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[0, 0],
        y=[min(dates) - 5, max(dates) + 5],
        mode="lines",
        line=dict(color="deeppink", width=3),
        showlegend=False,
    ))

    for xi, yi in zip(x_stem, dates):
        if int(yi) == 1993:
            fig.add_trace(go.Scatter(
                x=[-xi, xi], y=[yi, yi],
                mode="lines",
                line=dict(color="darkmagenta", width=2),
                showlegend=False,
            ))
        fig.add_trace(go.Scatter(
            x=[0, xi], y=[yi, yi],
            mode="lines",
            line=dict(color="darkmagenta", width=2),
            showlegend=False,
        ))

    for size, color in [(12, "palevioletred"), (6, "darkmagenta")]:
        fig.add_trace(go.Scatter(
            x=np.zeros(len(dates)),
            y=dates,
            mode="markers",
            marker=dict(size=size, color=color),
            showlegend=False,
        ))

    for xi, yi, label in zip(x_label, dates, labels):
        fig.add_trace(go.Scatter(
            x=[xi],
            y=[yi + 0.5],
            mode="text",
            text=[f"{label}, {int(yi)}"],
            textposition="middle right" if xi < 0 else "middle left",
            textfont=dict(family=FONT, size=12, color="#c9d1d9"),
            showlegend=False,
        ))

    fig.update_layout(
        title=dict(
            text="Important Milestones in AI",
            x=0.5,
            font=dict(family=FONT, size=16, color="#c9d1d9"),
        ),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        plot_bgcolor=BG,
        paper_bgcolor=BG,
        margin=dict(t=80, l=20, r=20, b=20),
        height=700,
    )
    fig.show()

    _evolution_hbar(
        evolution, "birthYear",
        "Subtopic birth year and volume comparison up to 2026",
        "Total Volume", [1945, 2026], "birthYear", "Birth year",
    ).show()

    evolution["volPerYear"] = (
        evolution.totalVolume / (2026 - evolution.birthYear)
    ).astype("int64")

    _evolution_hbar(
        evolution, "volPerYear",
        "Subtopic Volume per Year",
        "Volume per Year", None, None,"Volume per year",
    ).show()

    _print_block("VOLUME PER YEAR", evolution.volPerYear.describe(), width=32)

    _evolution_hbar(
        evolution, "avgYear",
        "Subtopic average year (by paper) and volume comparison up to 2026",
        "Total Volume", [2014, 2026], "avgYear", "Average year",
    ).show()

    df_before2011["collectionYear"] = 2010
    df_2011to2021["collectionYear"] = 2021
    df_from2021onwards["collectionYear"] = 2026
    df_from2021onwards.birthYear = df_before2011.birthYear
    df_2011to2021.birthYear = df_before2011.birthYear

    palette = [
        "#00C9A7", "#FF6B6B", "#8AACAA", "#FFE66D",
        "#A78BFA", "#F97316", "#00C43B", "#F20D5F",
    ]

    def _build_traces(d1, d2, d3):
        all_data = pd.concat([d1, d2, d3], ignore_index=True)
        traces = []
        for i, sub in enumerate(all_data["subtopic"].unique()):
            rows = all_data[
                all_data["subtopic"] == sub].sort_values("collectionYear")
            birth_year = rows["birthYear"].iloc[0]
            traces.append(go.Scatter(
                x=[birth_year] + rows["collectionYear"].tolist(),
                y=[0] + rows["totalVolume"].cumsum().tolist(),
                mode="lines+markers",
                name=sub,
                line=dict(color=palette[i % len(palette)], width=2.5,
                            shape="spline"),
                marker=dict(size=7, symbol="circle"),
            ))
        return traces

    fig = go.Figure(data=_build_traces(df_before2011, df_2011to2021,
                                        df_from2021onwards))
    fig.update_layout(
        title=dict(text="Volume by subtopic", x=0.04,
                    font=dict(size=18, color="#e6edf3")),
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family=FONT_MONO, color="#c9d1d9", size=12),
        xaxis=dict(title="Year", gridcolor=_GRID2, linecolor="#30363d",
                    tickcolor="#30363d", zeroline=False, tickformat="d"),
        yaxis=dict(title="Cumulative Volume", gridcolor=_GRID2,
                    linecolor="#30363d", tickcolor="#30363d",
                    zeroline=True, zerolinecolor="#30363d"),
        legend=dict(bgcolor="rgba(22,27,34,0.85)", bordercolor="#30363d",
                    borderwidth=1, x=0.02, y=0.98),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#161b22", bordercolor="#30363d",
                        font=dict(family=FONT_MONO, size=12)),
        margin=dict(t=60, r=30, b=60, l=70),
    )
    fig.show()

    evolution["gap"] = evolution["avgYear"].astype("int64") - \
        evolution["birthYear"]
    df_gap = evolution.sort_values("gap").reset_index(drop=True)

    fig = go.Figure()

    for _, row in df_gap.iterrows():
        fig.add_shape(
            type="line",
            x0=row["birthYear"], x1=row["avgYear"],
            y0=row["subtopic"], y1=row["subtopic"],
            line=dict(color="rgba(255,255,255,0.12)", width=6),
            layer="below",
        )

    for x_col, name, color in [
        ("birthYear", "Birth Year", _COLOR_TEAL),
        ("avgYear", "Avg Paper Year", _COLOR_RED),
    ]:
        fig.add_trace(go.Scatter(
            x=df_gap[x_col],
            y=df_gap["subtopic"],
            mode="markers",
            name=name,
            marker=dict(color=color, size=16, line=dict(color=BG, width=2)),
            hovertemplate=(
                f"<b>%{{y}}</b><br>{name}: %{{x}}"
                + ("<br>Gap: %{customdata} yrs" if x_col == "avgYear" else "")
                + "<extra></extra>"
            ),
            **({"customdata": df_gap["gap"]} if x_col == "avgYear" else {}),
        ))

    for _, row in df_gap.iterrows():
        fig.add_annotation(
            x=(row["birthYear"] + row["avgYear"]) / 2,
            y=row["subtopic"],
            text=f"+{row['gap']} yrs",
            showarrow=False,
            yshift=14,
            font=dict(size=10, color="rgba(200,200,200,0.6)", family=FONT_MONO),
        )

    fig.update_layout(
        title=dict(
            text="Birth year to Average paper year by subtopic",
            x=0.04,
            font=dict(size=18, color="#e6edf3", family=FONT_MONO),
        ),
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family=FONT_MONO, color="#c9d1d9", size=12),
        xaxis=dict(title="Year", gridcolor=_GRID2, linecolor="#30363d",
                    tickcolor="#30363d", zeroline=False, tickformat="d"),
        yaxis=dict(gridcolor=_GRID2, linecolor="#30363d",
                    tickcolor="#30363d", tickfont=dict(size=13)),
        legend=dict(bgcolor="rgba(22,27,34,0.85)", bordercolor="#30363d",
                    borderwidth=1, orientation="h", x=0.5, xanchor="center",
                    y=1.08),
        hovermode="y unified",
        margin=dict(t=80, r=40, b=60, l=100),
        height=120 + len(df_gap) * 60,
    )
    fig.show()

    _print_block("FIELDS OVERVIEW", funap_df, width=35)

    fig = px.pie(
        funap_df,
        names="type",
        values="count",
        title="Applied vs Fundamental Research by Paper Numbers",
        color_discrete_sequence=[_COLOR_TEAL, _COLOR_RED],
    )
    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>",
        marker=dict(line=dict(color=BG, width=2)),
    )
    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family=FONT_MONO, color="#c9d1d9", size=12),
        title=dict(x=0.5, font=dict(size=18, color="#e6edf3")),
        margin=dict(t=60, r=30, b=60, l=30),
    )
    fig.show()

    fund = funap_df[funap_df["type"] == "Fundamental"]["avgYear"].values[0]
    appl = funap_df[funap_df["type"] == "Applied"]["avgYear"].values[0]
    gap = round(appl - fund, 2)
    mid = (fund + appl) / 2

    fig = go.Figure()

    steps = 60
    for i in range(steps):
        t = i / steps
        x0 = fund + (appl - fund) * t
        x1 = fund + (appl - fund) * ((i + 1) / steps)
        r = int(0x4E + (0xFF - 0x4E) * t)
        g = int(0xCD + (0x6B - 0xCD) * t)
        b = int(0xC4 + (0x6B - 0xC4) * t)
        fig.add_shape(
            type="line",
            x0=x0, x1=x1, y0=0, y1=0,
            line=dict(color=f"rgb({r},{g},{b})", width=5),
            layer="below",
        )

    fig.add_shape(
        type="line",
        x0=fund, x1=appl, y0=0, y1=0,
        line=dict(color="rgba(255,255,255,0.04)", width=20),
        layer="below",
    )

    for x, color in [(fund, _COLOR_TEAL), (appl, _COLOR_RED)]:
        fig.add_shape(
            type="line",
            x0=x, x1=x, y0=-0.08, y1=0.08,
            line=dict(color=color, width=2),
        )

    fig.add_trace(go.Scatter(
        x=[fund, appl],
        y=[0, 0],
        mode="markers",
        marker=dict(color=[_COLOR_TEAL, _COLOR_RED], size=22,
                    line=dict(color=BG, width=3)),
        showlegend=False,
        hovertemplate="%{customdata}<br><b>%{x}</b><extra></extra>",
        customdata=["Fundamental", "Applied"],
    ))

    for x, label, color in [
        (fund, "FUNDAMENTAL", _COLOR_TEAL),
        (appl, "APPLIED", _COLOR_RED),
    ]:
        fig.add_annotation(x=x, y=0, text=f"<b>{label}</b>",
                            showarrow=False, yshift=38,
                            font=dict(size=13, color=color, family=FONT))
        fig.add_annotation(x=x, y=0, text=f"<b>{int(x)}</b>",
                            showarrow=False, yshift=18,
                            font=dict(size=22, color=color, family=FONT))

    fig.add_annotation(
        x=mid, y=0,
        text=f"<b>+{gap} yrs</b>",
        showarrow=False, yshift=-36,
        font=dict(size=13, color="rgba(200,210,220,0.65)", family=FONT),
        bgcolor="rgba(255,255,255,0.04)",
        bordercolor="rgba(255,255,255,0.10)",
        borderwidth=1, borderpad=6,
    )
    fig.add_annotation(
        x=appl - (appl - fund) * 0.07, y=0,
        ax=fund + (appl - fund) * 0.07, ay=0,
        axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1.2,
        arrowwidth=1.5, arrowcolor="rgba(255,255,255,0.15)",
        text="",
    )

    fig.update_layout(
        title=dict(
            text=(
                "<b>Applied vs Fundamental Research</b>"
                "<br><sup>Average publication year comparison</sup>"
            ),
            x=0.5, xanchor="center",
            font=dict(size=16, color="#e6edf3", family=FONT),
        ),
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family=FONT, color="#c9d1d9"),
        xaxis=dict(showgrid=False, zeroline=False, showline=False,
                    showticklabels=False, range=[fund - 1, appl + 1]),
        yaxis=dict(showgrid=False, zeroline=False, showline=False,
                    showticklabels=False, range=[-2, 2]),
        margin=dict(t=100, b=80, l=60, r=60),
        height=280,
        width=700,
    )
    fig.show()


def s8q1(affiliation_df: pd.DataFrame, citations_df: pd.DataFrame) -> None:
    _print_block("MISSING AFFILIATION OF PAPERS", affiliation_df, width=45)
    _print_block("AFFILIATION ANALYSIS", affiliation_df.describe(), width=20)

    fig = px.bar(
        affiliation_df,
        x="subtopic",
        y="count",
        color="count",
        title="# of Missing Affiliations by Subtopic",
        color_continuous_scale="Tealgrn",
    )
    fig.update_traces(
        text=affiliation_df["count"].round(2),
        textposition="outside",
        marker=dict(line=dict(color=BG, width=1.5)),
        hovertemplate="<b>%{x}</b><br>Missing affiliations: %{y:.2f}<extra></extra>",
    )
    fig.update_layout(**_base_layout(
        xaxis=_axis(tickangle=-20),
        yaxis=_axis("Missing Affiliations", grid=True),
        coloraxis_showscale=False,
        margin=dict(t=60, b=80, l=60, r=40),
    ))
    fig.show()

    _print_block("OVERVIEW OF CITATIONS IN CATEGORIES", citations_df, width=43)

    labels_left = list(citations_df.subtopic.unique())
    labels_right = list(citations_df.citationStatus.unique())
    idx = len(labels_left)
    tracked = citations_df.citationStatus == "Citations Tracked"

    def _counts(mask):
        return citations_df[mask]["count"].tolist()

    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=20,
            thickness=18,
            line=dict(color="rgba(255,255,255,0.15)", width=0.5),
            label=labels_left + labels_right,
            color=[_COLOR_TEAL] * len(labels_left) + \
                    [_COLOR_RED] * len(labels_right),
        ),
        link=dict(
            source=list(range(idx)) * 2,
            target=[idx] * idx + [idx + 1] * idx,
            value=_counts(tracked) + _counts(~tracked),
            color="rgba(255,255,255,0.15)",
            hovertemplate="Amount: %{value}<extra></extra>",
        ),
    )])
    fig.update_layout(**_base_layout(
        title=dict(
            text="Tracked Citations by Subtopic",
            x=0.5, xanchor="center",
            font=dict(size=18, color="#e6edf3", family=FONT),
        ),
        font=dict(color="#c9d1d9", family=FONT, size=12),
        margin=dict(t=90, b=40, l=40, r=40),
        height=500,
    ))
    fig.show()

    fig = go.Figure(data=[
        go.Bar(
            name="No Data",
            x=labels_left,
            y=_counts(~tracked),
            marker=dict(color=_COLOR_RED, line=dict(color=BG, width=1.5)),
            hovertemplate="<b>%{x}</b><br>No Data: %{y}<extra></extra>",
        ),
        go.Bar(
            name="Cited",
            x=labels_left,
            y=_counts(tracked),
            marker=dict(color=_COLOR_TEAL, line=dict(color=BG, width=1.5)),
            hovertemplate="<b>%{x}</b><br>Cited: %{y}<extra></extra>",
        ),
    ])
    fig.update_layout(**_base_layout(
        barmode="group",
        xaxis=_axis(tickangle=-20),
        yaxis=_axis("Count", grid=True),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h",
                    y=1.08, x=0.5, xanchor="center"),
        margin=dict(t=90, b=80, l=60, r=40),
    ))
    fig.show()
