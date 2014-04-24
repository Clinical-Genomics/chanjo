# -*- coding: utf-8 -*-
"""
    pygments.styles.solarized.light
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The Solarized style, inspired by Schoonover.

    :copyright: Copyright 2012 by the Shoji KUMAGAI, see AUTHORS.
    :license: MIT, see LICENSE for details.
"""

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Text, \
     Number, Operator, Generic, Whitespace, Other, Literal, Punctuation


class LightStyle(Style):
  """
  The Solarized Light style, inspired by Schoonover.
  """
  background_color = ''
  default_style = ""

  styles = {
    Text:                   '#657b83',             # base00 ; class: ''
    Whitespace:             '#fdf6e3',             # base3  ; class: 'w'
    Error:                  '#dc322f',             # red    ; class: 'err'
    Other:                  '#657b83',             # base00 ; class: 'x'

    Comment:                'italic #93a1a1',      # base1  ; class: 'c'
    Comment.Multiline:      'italic #93a1a1',      # base1  ; class: 'cm'
    Comment.Preproc:        'italic #93a1a1',      # base1  ; class: 'cp'
    Comment.Single:         'italic #93a1a1',      # base1  ; class: 'c1'
    Comment.Special:        'italic #93a1a1',      # base1  ; class: 'cs'

    Keyword:                '#859900',             # green  ; class: 'k'
    Keyword.Constant:       '#859900',             # green  ; class: 'kc'
    Keyword.Declaration:    '#859900',             # green  ; class: 'kd'
    Keyword.Namespace:      '#cb4b16',             # orange ; class: 'kn'
    Keyword.Pseudo:         '#cb4b16',             # orange ; class: 'kp'
    Keyword.Reserved:       '#859900',             # green  ; class: 'kr'
    Keyword.Type:           '#859900',             # green  ; class: 'kt'

    Operator:               '#657b83',             # base00 ; class: 'o'
    Operator.Word:          '#859900',             # green  ; class: 'ow'

    Name:                   '#586e75',             # base01 ; class: 'n'
    Name.Attribute:         '#657b83',             # base00 ; class: 'na'
    Name.Builtin:           '#268bd2',             # blue   ; class: 'nb'
    Name.Builtin.Pseudo:    'bold #268bd2',        # blue   ; class: 'bp'
    Name.Class:             '#268bd2',             # blue   ; class: 'nc'
    Name.Constant:          '#b58900',             # yellow ; class: 'no'
    Name.Decorator:         '#cb4b16',             # orange ; class: 'nd'
    Name.Entity:            '#cb4b16',             # orange ; class: 'ni'
    Name.Exception:         '#cb4b16',             # orange ; class: 'ne'
    Name.Function:          '#268bd2',             # blue   ; class: 'nf'
    Name.Property:          '#268bd2',             # blue   ; class: 'py'
    Name.Label:             '#657b83',             # base00 ; class: 'nc'
    Name.Namespace:         '#b58900',             # yellow ; class: 'nn'
    Name.Other:             '#657b83',             # base00 ; class: 'nx'
    Name.Tag:               '#859900',             # green  ; class: 'nt'
    Name.Variable:          '#cb4b16',             # orange ; class: 'nv'
    Name.Variable.Class:    '#268bd2',             # blue   ; class: 'vc'
    Name.Variable.Global:   '#268bd2',             # blue   ; class: 'vg'
    Name.Variable.Instance: '#268bd2',             # blue   ; class: 'vi'

    Number:                 '#2aa198',             # cyan   ; class: 'm'
    Number.Float:           '#2aa198',             # cyan   ; class: 'mf'
    Number.Hex:             '#2aa198',             # cyan   ; class: 'mh'
    Number.Integer:         '#2aa198',             # cyan   ; class: 'mi'
    Number.Integer.Long:    '#2aa198',             # cyan   ; class: 'il'
    Number.Oct:             '#2aa198',             # cyan   ; class: 'mo'

    Literal:                '#657b83',             # base00 ; class: 'l'
    Literal.Date:           '#657b83',             # base00 ; class: 'ld'

    Punctuation:            '#657b83',             # base00 ; class: 'p'

    String:                 '#2aa198',             # cyan   ; class: 's'
    String.Backtick:        '#2aa198',             # cyan   ; class: 'sb'
    String.Char:            '#2aa198',             # cyan   ; class: 'sc'
    String.Doc:             '#2aa198',             # cyan   ; class: 'sd'
    String.Double:          '#2aa198',             # cyan   ; class: 's2'
    String.Escape:          '#cb4b16',             # orange ; class: 'se'
    String.Heredoc:         '#2aa198',             # cyan   ; class: 'sh'
    String.Interpol:        '#cb4b16',             # orange ; class: 'si'
    String.Other:           '#2aa198',             # cyan   ; class: 'sx'
    String.Regex:           '#2aa198',             # cyan   ; class: 'sr'
    String.Single:          '#2aa198',             # cyan   ; class: 's1'
    String.Symbol:          '#2aa198',             # cyan   ; class: 'ss'

    Generic:                '#657b83',             # base00 ; class: 'g'
    Generic.Deleted:        '#657b83',             # base00 ; class: 'gd'
    Generic.Emph:           '#657b83',             # base00 ; class: 'ge'
    Generic.Error:          '#657b83',             # base00 ; class: 'gr'
    Generic.Heading:        '#657b83',             # base00 ; class: 'gh'
    Generic.Inserted:       '#657b83',             # base00 ; class: 'gi'
    Generic.Output:         '#657b83',             # base00 ; class: 'go'
    Generic.Prompt:         '#657b83',             # base00 ; class: 'gp'
    Generic.Strong:         '#657b83',             # base00 ; class: 'gs'
    Generic.Subheading:     '#657b83',             # base00 ; class: 'gu'
    Generic.Traceback:      '#657b83',             # base00 ; class: 'gt'
  }


class DarkStyle(Style):
  """
  The Solarized Dark style, inspired by Schoonover.
  """
  background_color = '#002b36'
  default_style = ""

  styles = {
    Text:                   '#839496',             # base0  ; class: ''
    Whitespace:             '#002b36',             # base03 ; class: 'w'
    Error:                  '#dc322f',             # red    ; class: 'err'
    Other:                  '#839496',             # base0  ; class: 'x'

    Comment:                'italic #586e75',      # base01 ; class: 'c'
    Comment.Multiline:      'italic #586e75',      # base01 ; class: 'cm'
    Comment.Preproc:        'italic #586e75',      # base01 ; class: 'cp'
    Comment.Single:         'italic #586e75',      # base01 ; class: 'c1'
    Comment.Special:        'italic #586e75',      # base01 ; class: 'cs'

    Keyword:                '#859900',             # green  ; class: 'k'
    Keyword.Constant:       '#859900',             # green  ; class: 'kc'
    Keyword.Declaration:    '#859900',             # green  ; class: 'kd'
    Keyword.Namespace:      '#cb4b16',             # orange ; class: 'kn'
    Keyword.Pseudo:         '#cb4b16',             # orange ; class: 'kp'
    Keyword.Reserved:       '#859900',             # green  ; class: 'kr'
    Keyword.Type:           '#859900',             # green  ; class: 'kt'

    Operator:               '#839496',             # base0  ; class: 'o'
    Operator.Word:          '#859900',             # green  ; class: 'ow'

    Name:                   '#93a1a1',             # base1  ; class: 'n'
    Name.Attribute:         '#839496',             # base0  ; class: 'na'
    Name.Builtin:           '#268bd2',             # blue   ; class: 'nb'
    Name.Builtin.Pseudo:    'bold #268bd2',        # blue   ; class: 'bp'
    Name.Class:             '#268bd2',             # blue   ; class: 'nc'
    Name.Constant:          '#b58900',             # yellow ; class: 'no'
    Name.Decorator:         '#cb4b16',             # orange ; class: 'nd'
    Name.Entity:            '#cb4b16',             # orange ; class: 'ni'
    Name.Exception:         '#cb4b16',             # orange ; class: 'ne'
    Name.Function:          '#268bd2',             # blue   ; class: 'nf'
    Name.Property:          '#268bd2',             # blue   ; class: 'py'
    Name.Label:             '#839496',             # base0  ; class: 'nc'
    Name.Namespace:         '#b58900',             # yellow ; class: 'nn'
    Name.Other:             '#839496',             # base0  ; class: 'nx'
    Name.Tag:               '#859900',             # green  ; class: 'nt'
    Name.Variable:          '#cb4b16',             # orange ; class: 'nv'
    Name.Variable.Class:    '#268bd2',             # blue   ; class: 'vc'
    Name.Variable.Global:   '#268bd2',             # blue   ; class: 'vg'
    Name.Variable.Instance: '#268bd2',             # blue   ; class: 'vi'

    Number:                 '#2aa198',             # cyan   ; class: 'm'
    Number.Float:           '#2aa198',             # cyan   ; class: 'mf'
    Number.Hex:             '#2aa198',             # cyan   ; class: 'mh'
    Number.Integer:         '#2aa198',             # cyan   ; class: 'mi'
    Number.Integer.Long:    '#2aa198',             # cyan   ; class: 'il'
    Number.Oct:             '#2aa198',             # cyan   ; class: 'mo'

    Literal:                '#839496',             # base0  ; class: 'l'
    Literal.Date:           '#839496',             # base0  ; class: 'ld'

    Punctuation:            '#839496',             # base0  ; class: 'p'

    String:                 '#2aa198',             # cyan   ; class: 's'
    String.Backtick:        '#2aa198',             # cyan   ; class: 'sb'
    String.Char:            '#2aa198',             # cyan   ; class: 'sc'
    String.Doc:             '#2aa198',             # cyan   ; class: 'sd'
    String.Double:          '#2aa198',             # cyan   ; class: 's2'
    String.Escape:          '#cb4b16',             # orange ; class: 'se'
    String.Heredoc:         '#2aa198',             # cyan   ; class: 'sh'
    String.Interpol:        '#cb4b16',             # orange ; class: 'si'
    String.Other:           '#2aa198',             # cyan   ; class: 'sx'
    String.Regex:           '#2aa198',             # cyan   ; class: 'sr'
    String.Single:          '#2aa198',             # cyan   ; class: 's1'
    String.Symbol:          '#2aa198',             # cyan   ; class: 'ss'

    Generic:                '#839496',             # base0  ; class: 'g'
    Generic.Deleted:        '#839496',             # base0  ; class: 'gd'
    Generic.Emph:           '#839496',             # base0  ; class: 'ge'
    Generic.Error:          '#839496',             # base0  ; class: 'gr'
    Generic.Heading:        '#839496',             # base0  ; class: 'gh'
    Generic.Inserted:       '#839496',             # base0  ; class: 'gi'
    Generic.Output:         '#839496',             # base0  ; class: 'go'
    Generic.Prompt:         '#839496',             # base0  ; class: 'gp'
    Generic.Strong:         '#839496',             # base0  ; class: 'gs'
    Generic.Subheading:     '#839496',             # base0  ; class: 'gu'
    Generic.Traceback:      '#839496',             # base0  ; class: 'gt'
  }
