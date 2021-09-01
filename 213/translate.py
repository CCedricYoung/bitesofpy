import re


example = """
this
<code>is✅</code>
some
<code>
code to✅
 </code>
process
  <code>
    now✅
</code>
Done
"""

example2 = """
1this
<code>2is</code>
3some
<code>
4code to
 </code>
5process
  <code>
    6now
</code>
7Done
"""

def fix_translation(org_text, trans_text):
    """Receives original English text as well as text returned by translator.
       Parse trans_text restoring the original (English) code (wrapped inside
       code and pre tags) into it. Return the fixed translation str
    """
    codes_re = re.compile(r'<code>.*?</code>|<pre>.*?</pre>', re.DOTALL)
    codes = codes_re.findall(org_text)
    return codes_re.sub(lambda _: codes.pop(0), trans_text)

print(fix_translation(example, example2))
