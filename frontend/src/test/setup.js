import '@testing-library/jest-dom/vitest';

// JSDOM Polyfills for React Three Fiber and WebGL canvas testing
if (typeof window !== 'undefined') {
  class ResizeObserverMock {
    observe() {}
    unobserve() {}
    disconnect() {}
  }
  window.ResizeObserver = window.ResizeObserver || ResizeObserverMock;
  global.ResizeObserver = global.ResizeObserver || ResizeObserverMock;

  // Mock HTMLCanvasElement.getContext for WebGL/2D in JSDOM
  HTMLCanvasElement.prototype.getContext = function (type) {
    if (type === 'webgl' || type === 'webgl2' || type === 'experimental-webgl') {
      return {
        getExtension: () => null,
        getParameter: () => 0,
        createShader: () => ({}),
        shaderSource: () => {},
        compileShader: () => {},
        getShaderParameter: () => true,
        createProgram: () => ({}),
        attachShader: () => {},
        linkProgram: () => {},
        getProgramParameter: () => true,
        useProgram: () => {},
        createBuffer: () => ({}),
        bindBuffer: () => {},
        bufferData: () => {},
        enable: () => {},
        disable: () => {},
        clear: () => {},
        clearColor: () => {},
        viewport: () => {},
        drawArrays: () => {},
        drawElements: () => {},
      };
    }
    return null;
  };
}
