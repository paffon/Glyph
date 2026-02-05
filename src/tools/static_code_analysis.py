"""
Static code analysis tool for analyzing source code files.
Supports multiple languages through pluggable parsers.
"""
import os
import statistics
from typing import Dict, List, Any, Optional

from mcp_object import mcp
from response import GlyphMCPResponse
from tools._utils import validate_absolute_path
from tools.parsers.base_parser import BaseParser
from tools.parsers.python_parser import PythonParser
from tools.parsers.csharp_parser import CSharpParser
from tools.parsers.shared_models import FileMetrics


# Registry of available parsers
PARSERS: List[BaseParser] = [
    CSharpParser(),  # C# first as per user preference
    PythonParser(),
]

# Map of file extensions to parser
EXTENSION_MAP: Dict[str, BaseParser] = {}
for parser in PARSERS:
    for ext in parser.file_extensions:
        EXTENSION_MAP[ext.lower()] = parser


def get_parser_for_file(file_path: str) -> Optional[BaseParser]:
    """Get the appropriate parser for a file based on its extension."""
    ext = os.path.splitext(file_path)[1].lower()
    return EXTENSION_MAP.get(ext)


def get_supported_extensions() -> List[str]:
    """Get list of all supported file extensions."""
    return list(EXTENSION_MAP.keys())


def get_minimal_unique_paths(file_paths: List[str]) -> Dict[str, str]:
    """
    Generate minimal unique paths for a list of file paths.
    Returns a dict mapping full path to minimal unique suffix.
    """
    if not file_paths:
        return {}
    
    # Normalize paths to use forward slashes
    normalized = {p: p.replace('\\', '/') for p in file_paths}
    
    # Split each path into components (in reverse order)
    path_components = {}
    for full_path, norm_path in normalized.items():
        parts = norm_path.split('/')
        path_components[full_path] = list(reversed(parts))
    
    # Build minimal paths by adding components until unique
    minimal_paths = {}
    for full_path in file_paths:
        components = path_components[full_path]
        
        # Start with just the filename
        for depth in range(1, len(components) + 1):
            candidate = '/'.join(reversed(components[:depth]))
            
            # Check if this candidate is unique
            is_unique = True
            for other_path in file_paths:
                if other_path == full_path:
                    continue
                other_components = path_components[other_path]
                other_candidate = '/'.join(reversed(other_components[:depth]))
                if candidate == other_candidate:
                    is_unique = False
                    break
            
            if is_unique:
                minimal_paths[full_path] = candidate
                break
        else:
            # Fallback to full path if no unique suffix found
            minimal_paths[full_path] = normalized[full_path]
    
    return minimal_paths


def format_methods_table(all_metrics: List[Dict[str, Any]]) -> str:
    """Generate a consolidated table of all methods across all files and classes."""
    # Get minimal unique paths
    file_paths = [m['path'] for m in all_metrics]
    minimal_paths = get_minimal_unique_paths(file_paths)
    
    # Collect all methods
    rows = []
    for file_metrics in all_metrics:
        file_path = file_metrics['path']
        minimal_file = minimal_paths[file_path]
        
        # Process classes and their methods
        for cls in file_metrics.get('classes', []):
            class_name = cls['name']
            for method in cls.get('methods', []):
                rows.append({
                    'file': minimal_file,
                    'class': class_name,
                    'method': method['name'],
                    'lines': method['lines']['count'],
                    'arguments': method['arg_count'],
                    'access': method.get('access_modifier', ''),
                    'return_type': method.get('return_type', ''),
                    'async': method.get('is_async', False),
                    'static': method.get('is_static', False),
                    'line_stats': method['line_length_stats']
                })
        
        # Process top-level functions
        for func in file_metrics.get('functions', []):
            rows.append({
                'file': minimal_file,
                'class': '',
                'method': func['name'],
                'lines': func['lines']['count'],
                'arguments': func['arg_count'],
                'access': func.get('access_modifier', ''),
                'return_type': func.get('return_type', ''),
                'async': func.get('is_async', False),
                'static': func.get('is_static', False),
                'line_stats': func['line_length_stats']
            })
    
    if not rows:
        return ""
    
    result = [
        "## Consolidated Methods/Functions Table",
        "",
        "| File | Class | Method | Lines | Arguments | Access | Return Type | LL Min | LL Max | LL Mean | LL Median | LL Std |",
        "| - | - | - | - | - | - | - | - | - | - | - | - |",
    ]
    
    for row in rows:
        stats = row['line_stats']
        file_display = f"`{row['file']}`"
        class_display = f"`{row['class']}`" if row['class'] else ""
        method_display = f"`{row['method']}`"
        access_display = row['access'] if row['access'] else ""
        return_display = f"`{row['return_type']}`" if row['return_type'] else ""
        
        result.append(
            f"| {file_display} | {class_display} | {method_display} | {row['lines']} | "
            f"{row['arguments']} | {access_display} | {return_display} | "
            f"{stats['min']} | {stats['max']} | {stats['mean']} | {stats['median']} | {stats['std']} |"
        )
    
    result.append("")
    return "\n".join(result)


def format_line_stats_table(stats: Dict[str, Any], indent: str = "") -> str:
    """Format line statistics as a table row."""
    return (
        f"{indent}| count | min | max | mean | median | std |\n"
        f"{indent}| - | - | - | - | - | - |\n"
        f"{indent}| {stats['count']} | {stats['min']} | {stats['max']} | "
        f"{stats['mean']} | {stats['median']} | {stats['std']} |"
    )


def format_method_markdown(method: Dict[str, Any], indent: str = "") -> str:
    """Format method metrics as markdown."""
    lines = method['lines']
    result = [
        f"{indent}##### `{method['name']}`",
        f"{indent}- **Lines**: {lines['start']}-{lines['end']} ({lines['count']} lines)",
        f"{indent}- **Arguments**: {method['arg_count']}",
    ]
    
    # Add optional fields
    if method.get('access_modifier'):
        result.append(f"{indent}- **Access**: {method['access_modifier']}")
    if method.get('return_type'):
        result.append(f"{indent}- **Return Type**: `{method['return_type']}`")
    if method.get('is_async'):
        result.append(f"{indent}- **Async**: Yes")
    if method.get('is_static'):
        result.append(f"{indent}- **Static**: Yes")
    
    result.extend([
        f"{indent}- **Line Length Statistics**:",
        format_line_stats_table(method['line_length_stats'], indent + "  ")
    ])
    return "\n".join(result)


def format_class_markdown(cls: Dict[str, Any]) -> str:
    """Format class metrics as markdown."""
    lines = cls['lines']
    result = [
        f"#### Class: `{cls['name']}`",
        f"- **Lines**: {lines['start']}-{lines['end']} ({lines['count']} lines)",
        f"- **Constructor Parameters**: {cls['constructor_param_count']}",
        f"- **Method Count**: {cls['method_count']}",
    ]
    
    # Add optional fields
    if cls.get('access_modifier'):
        result.append(f"- **Access**: {cls['access_modifier']}")
    if cls.get('property_count', 0) > 0:
        result.append(f"- **Property Count**: {cls['property_count']}")
    if cls.get('is_abstract'):
        result.append(f"- **Abstract**: Yes")
    if cls.get('is_static'):
        result.append(f"- **Static**: Yes")
    if cls.get('base_classes'):
        result.append(f"- **Base Classes**: {', '.join(cls['base_classes'])}")
    if cls.get('interfaces'):
        result.append(f"- **Interfaces**: {', '.join(cls['interfaces'])}")
    
    result.extend([
        f"- **Line Length Statistics**:",
        format_line_stats_table(cls['line_length_stats'], "  "),
        ""
    ])
    
    if cls.get('methods'):
        result.append("**Methods:**\n")
        for method in cls['methods']:
            result.append(format_method_markdown(method, ""))
            result.append("")
    
    return "\n".join(result)


def format_file_markdown(file_metrics: Dict[str, Any]) -> str:
    """Format file metrics as markdown."""
    result = [
        f"### File: `{file_metrics['path']}`",
        f"- **Language**: {file_metrics['language']}",
        f"- **Total Lines**: {file_metrics['line_count']}",
        f"- **Classes**: {file_metrics['class_count']}",
        f"- **Top-level Functions**: {file_metrics['function_count']}",
    ]
    
    # Add optional fields
    if file_metrics.get('namespaces'):
        result.append(f"- **Namespaces**: {', '.join(file_metrics['namespaces'])}")
    if file_metrics.get('using_statements'):
        result.append(f"- **Using Statements**: {len(file_metrics['using_statements'])}")
    
    if file_metrics.get('parse_error'):
        result.append(f"- **Parse Error**: {file_metrics['parse_error']}")
    
    result.extend([
        f"- **Line Length Statistics**:",
        format_line_stats_table(file_metrics['line_length_stats'], "  "),
        ""
    ])
    
    if file_metrics.get('classes'):
        result.append("#### Classes\n")
        for cls in file_metrics['classes']:
            result.append(format_class_markdown(cls))
    
    if file_metrics.get('functions'):
        result.append("#### Top-level Functions\n")
        for func in file_metrics['functions']:
            result.append(format_method_markdown(func, ""))
            result.append("")
    
    return "\n".join(result)


def format_summary_markdown(all_metrics: List[Dict[str, Any]]) -> str:
    """Generate a summary section with aggregated statistics."""
    total_lines = sum(m['line_count'] for m in all_metrics)
    total_classes = sum(m['class_count'] for m in all_metrics)
    total_functions = sum(m['function_count'] for m in all_metrics)
    
    # Count files by language
    languages = {}
    for m in all_metrics:
        lang = m['language']
        languages[lang] = languages.get(lang, 0) + 1
    
    # Aggregate all metrics
    all_method_line_counts = []
    all_class_line_counts = []
    all_method_arg_counts = []
    all_constructor_param_counts = []
    all_property_counts = []
    
    for m in all_metrics:
        if m.get('classes'):
            for cls in m['classes']:
                all_class_line_counts.append(cls['lines']['count'])
                all_constructor_param_counts.append(cls['constructor_param_count'])
                if cls.get('property_count', 0) > 0:
                    all_property_counts.append(cls['property_count'])
                for method in cls.get('methods', []):
                    all_method_line_counts.append(method['lines']['count'])
                    all_method_arg_counts.append(method['arg_count'])
        
        if m.get('functions'):
            for func in m['functions']:
                all_method_line_counts.append(func['lines']['count'])
                all_method_arg_counts.append(func['arg_count'])
    
    result = [
        "## Summary Statistics",
        "",
        "### Overview",
        f"- **Total Files Analyzed**: {len(all_metrics)}",
    ]
    
    # Language breakdown
    for lang, count in sorted(languages.items()):
        result.append(f"  - {lang.title()}: {count} files")
    
    result.extend([
        f"- **Total Lines**: {total_lines}",
        f"- **Total Classes**: {total_classes}",
        f"- **Total Functions/Methods**: {total_functions + sum(len(m.get('classes', [])) for m in all_metrics)}",
        ""
    ])
    
    # Build a single consolidated metrics table
    categories = []
    if all_method_line_counts:
        categories.append(("Function/Method Line Counts", all_method_line_counts))
    if all_class_line_counts:
        categories.append(("Class Line Counts", all_class_line_counts))
    if all_method_arg_counts:
        categories.append(("Function/Method Argument Counts", all_method_arg_counts))
    if all_constructor_param_counts:
        categories.append(("Class Constructor Parameter Counts", all_constructor_param_counts))
    if all_property_counts:
        categories.append(("Class Property Counts", all_property_counts))
    
    if categories:
        result.append("### Metrics Summary")
        result.append("")
        
        # Build header
        header = "| Category | Count | Min | Max | Mean | Median | Std |"
        separator = "| - | - | - | - | - | - | - |"
        
        result.append(header)
        result.append(separator)
        
        # Build rows (one per category)
        for cat_name, values in categories:
            count = len(values)
            min_val = min(values)
            max_val = max(values)
            mean_val = round(statistics.mean(values), 2)
            median_val = round(statistics.median(values), 2)
            std_val = round(statistics.stdev(values), 2) if count > 1 else 0
            
            row = f"| {cat_name} | {count} | {min_val} | {max_val} | {mean_val} | {median_val} | {std_val} |"
            result.append(row)
        
        result.append("")
    
    return "\n".join(result)


def format_analysis_markdown(all_metrics: List[Dict[str, Any]]) -> str:
    """Format the complete analysis as markdown."""
    result = [
        "# Static Code Analysis Report",
        "",
        format_summary_markdown(all_metrics),
        "",
        format_methods_table(all_metrics),
        "",
        "## Detailed File Analysis",
        ""
    ]
    
    # Group by language for better organization
    by_language: Dict[str, List[Dict[str, Any]]] = {}
    for m in all_metrics:
        lang = m['language']
        if lang not in by_language:
            by_language[lang] = []
        by_language[lang].append(m)
    
    for lang in sorted(by_language.keys()):
        result.append(f"### {lang.title()} Files\n")
        for file_metrics in by_language[lang]:
            result.append(format_file_markdown(file_metrics))
            result.append("\n---\n")
    
    return "\n".join(result)


@mcp.tool()
def static_code_analysis(
    file_paths: List[str],
    save_to_ad_hoc: bool = False
) -> GlyphMCPResponse[Dict[str, Any]]:
    """
    Perform static code analysis on source code files.
    
    Supports multiple languages (C#, Python) through dedicated parsers.
    
    Analyzes files to produce metrics including:
    - Lines per file/method/class
    - Min, max, mean, median, and std of line lengths per file/method/class
    - Number of parameters per class (constructor args)
    - Number of arguments per method/function
    - Language-specific metrics (e.g., properties for C#)
    
    Args:
        file_paths: List of absolute paths to source files to analyze.
                   Supported extensions: .py (Python), .cs (C#)
        save_to_ad_hoc: If True, saves the analysis as a markdown file to .assistant/ad_hoc directory.
                       If False, returns the analysis as structured data.
    
    Returns:
        GlyphMCPResponse containing the analysis results.
        - If save_to_ad_hoc is True: confirms the file was written
        - If save_to_ad_hoc is False: returns the full analysis data
    """
    response = GlyphMCPResponse[Dict[str, Any]]()
    
    if not file_paths:
        response.add_context("No files provided for analysis.")
        return response
    
    # Validate all paths are absolute
    for path in file_paths:
        if not validate_absolute_path(path, response):
            return response
    
    supported_extensions = get_supported_extensions()
    response.add_context(f"Supported file types: {', '.join(supported_extensions)}")
    
    # Analyze each file
    all_metrics: List[FileMetrics] = []
    for file_path in file_paths:
        if not os.path.exists(file_path):
            response.add_context(f"File not found: {file_path}")
            continue
        
        parser = get_parser_for_file(file_path)
        if parser is None:
            response.add_context(f"Skipping unsupported file type: {file_path}")
            continue
        
        metrics = parser.parse_file(file_path)
        all_metrics.append(metrics)
        response.add_context(f"Analyzed ({parser.language_name}): {file_path}")
    
    if not all_metrics:
        response.add_context("No supported files were successfully analyzed.")
        return response
    
    # Convert to dict for output
    metrics_dicts = [m.to_dict() for m in all_metrics]
    
    if save_to_ad_hoc:
        # Generate markdown and save to .assistant/ad_hoc directory
        markdown_content = format_analysis_markdown(metrics_dicts)
        
        try:
            # Find .assistant directory by looking up from the first file's directory
            first_file = file_paths[0]
            current_dir = os.path.dirname(os.path.abspath(first_file))
            
            # Search for .assistant directory
            assistant_dir = None
            while current_dir:
                potential_assistant = os.path.join(current_dir, '.assistant')
                if os.path.isdir(potential_assistant):
                    assistant_dir = potential_assistant
                    break
                parent = os.path.dirname(current_dir)
                if parent == current_dir:  # reached root
                    break
                current_dir = parent
            
            if not assistant_dir:
                response.add_context("Could not find .assistant directory in parent directories.")
                return response
            
            # Create ad_hoc directory if it doesn't exist
            ad_hoc_dir = os.path.join(assistant_dir, 'ad_hoc')
            os.makedirs(ad_hoc_dir, exist_ok=True)
            
            # Generate filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"code_analysis_{timestamp}.md"
            output_path = os.path.join(ad_hoc_dir, filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            response.add_context(f"Analysis saved to: {output_path}")
            response.success = True
            response.result = {"output_path": output_path, "files_analyzed": len(metrics_dicts)}
        except Exception as e:
            response.add_context(f"Failed to write output file: {str(e)}")
    else:
        # Return the full analysis data
        response.success = True
        
        # Count by language
        language_counts = {}
        for m in metrics_dicts:
            lang = m['language']
            language_counts[lang] = language_counts.get(lang, 0) + 1
        
        response.result = {
            "files": metrics_dicts,
            "summary": {
                "total_files": len(metrics_dicts),
                "by_language": language_counts,
                "total_lines": sum(m['line_count'] for m in metrics_dicts),
                "total_classes": sum(m['class_count'] for m in metrics_dicts),
                "total_functions": sum(m['function_count'] for m in metrics_dicts)
            }
        }
    
    return response