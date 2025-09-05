window.clientside = {
  sum3: function(a, b, c) {
    // parseFloat(null) → NaN, so we fallback to 0
    a = parseFloat(a) || 0;
    b = parseFloat(b) || 0;
    c = parseFloat(c) || 0;
    return a + b + c;
  }
}