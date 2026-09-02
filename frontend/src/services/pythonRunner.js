let pyodide = null;

export async function initializePython() {
  if (!pyodide) {
    if (typeof window.loadPyodide !== "function") {
      throw new Error("Pyodide failed to load.");
    }

    pyodide = await window.loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.27.2/full/",
    });
  }

  return pyodide;
}

export async function runPython(code) {
  const python = await initializePython();

  const wrappedCode = `
  import sys
  from io import StringIO

  __stdout = sys.stdout
  __stderr = sys.stderr

  sys.stdout = StringIO()
  sys.stderr = StringIO()

  try:
      exec(${JSON.stringify(code)})
      __output = sys.stdout.getvalue()
      __error = sys.stderr.getvalue()
  finally:
      sys.stdout = __stdout
      sys.stderr = __stderr

  (__output, __error)
  `;

    return await python.runPythonAsync(wrappedCode);
}