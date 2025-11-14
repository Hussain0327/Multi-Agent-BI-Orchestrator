"""
Chart generation using matplotlib.

Converts ChartSpec objects from agent outputs into PNG images
suitable for embedding in PowerPoint or Excel.
"""

import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
from typing import Optional
import io
from PIL import Image

# Use non-interactive backend
matplotlib.use('Agg')

from src.schemas import ChartSpec


class ChartGenerator:
    """Generate charts from ChartSpec specifications."""

    def __init__(self, dpi: int = 150, figsize: tuple = (10, 6)):
        """
        Initialize chart generator.

        Args:
            dpi: Resolution of generated images
            figsize: Default figure size (width, height) in inches
        """
        self.dpi = dpi
        self.figsize = figsize

        # Default color palette (Valtric colors)
        self.default_colors = [
            "#3498DB",  # Blue (primary)
            "#2ECC71",  # Green (success)
            "#E74C3C",  # Red (warning)
            "#F39C12",  # Orange (accent)
            "#9B59B6",  # Purple
            "#1ABC9C",  # Turquoise
        ]

    def generate(
        self,
        chart_spec: ChartSpec,
        output_path: Optional[str] = None,
        return_bytes: bool = False
    ):
        """
        Generate chart from specification.

        Args:
            chart_spec: Chart specification from agent output
            output_path: Optional path to save PNG file
            return_bytes: If True, return image bytes instead of path

        Returns:
            Path to saved image or bytes if return_bytes=True
        """
        # Create figure
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        # Set colors
        colors = chart_spec.colors if chart_spec.colors else self.default_colors

        # Generate chart based on type
        if chart_spec.type == "bar":
            self._generate_bar(ax, chart_spec, colors)
        elif chart_spec.type == "line":
            self._generate_line(ax, chart_spec, colors)
        elif chart_spec.type == "scatter":
            self._generate_scatter(ax, chart_spec, colors)
        elif chart_spec.type == "pie":
            self._generate_pie(ax, chart_spec, colors)
        elif chart_spec.type == "area":
            self._generate_area(ax, chart_spec, colors)
        else:
            raise ValueError(f"Unsupported chart type: {chart_spec.type}")

        # Set title and labels
        ax.set_title(chart_spec.title, fontsize=16, fontweight='bold', pad=20)
        if chart_spec.x_label:
            ax.set_xlabel(chart_spec.x_label, fontsize=12)
        if chart_spec.y_label:
            ax.set_ylabel(chart_spec.y_label, fontsize=12)

        # Apply styling
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Tight layout
        plt.tight_layout()

        # Save or return bytes
        if return_bytes:
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=self.dpi, bbox_inches='tight')
            buf.seek(0)
            plt.close(fig)
            return buf.getvalue()
        else:
            if not output_path:
                output_path = f"chart_{chart_spec.type}_{id(chart_spec)}.png"

            plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
            plt.close(fig)
            return output_path

    def _generate_bar(self, ax, spec: ChartSpec, colors):
        """Generate bar chart."""
        bars = ax.bar(spec.x_data, spec.y_data, color=colors[:len(spec.x_data)])

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.,
                height,
                f'{height:,.0f}',
                ha='center',
                va='bottom',
                fontsize=10
            )

    def _generate_line(self, ax, spec: ChartSpec, colors):
        """Generate line chart."""
        ax.plot(
            spec.x_data,
            spec.y_data,
            color=colors[0],
            linewidth=2.5,
            marker='o',
            markersize=6
        )

        # Add value labels at points
        for x, y in zip(spec.x_data, spec.y_data):
            ax.text(x, y, f'{y:,.0f}', ha='center', va='bottom', fontsize=9)

    def _generate_scatter(self, ax, spec: ChartSpec, colors):
        """Generate scatter plot."""
        ax.scatter(
            spec.x_data,
            spec.y_data,
            color=colors[0],
            s=100,
            alpha=0.6,
            edgecolors='black',
            linewidth=1
        )

    def _generate_pie(self, ax, spec: ChartSpec, colors):
        """Generate pie chart."""
        wedges, texts, autotexts = ax.pie(
            spec.y_data,
            labels=spec.x_data,
            colors=colors[:len(spec.x_data)],
            autopct='%1.1f%%',
            startangle=90
        )

        # Enhance text
        for text in texts:
            text.set_fontsize(11)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)

    def _generate_area(self, ax, spec: ChartSpec, colors):
        """Generate area chart."""
        ax.fill_between(
            spec.x_data,
            spec.y_data,
            color=colors[0],
            alpha=0.3
        )
        ax.plot(
            spec.x_data,
            spec.y_data,
            color=colors[0],
            linewidth=2
        )

    def generate_metric_comparison(
        self,
        metrics: dict,
        title: str = "Key Metrics",
        output_path: Optional[str] = None
    ):
        """
        Generate a bar chart comparing multiple metrics.

        Args:
            metrics: Dict of metric_name: value
            title: Chart title
            output_path: Where to save

        Returns:
            Path to saved chart
        """
        from src.schemas import ChartSpec

        spec = ChartSpec(
            type="bar",
            title=title,
            x_label="Metric",
            y_label="Value",
            x_data=list(metrics.keys()),
            y_data=list(metrics.values())
        )

        return self.generate(spec, output_path)
