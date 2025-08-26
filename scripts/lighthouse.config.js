module.exports = {
  extends: 'lighthouse:default',
  settings: {
    // Emulate a consistent desktop environment
    emulatedFormFactor: 'desktop',
    throttling: {
      // Approximate fast 3G network
      rttMs: 40,
      throughputKbps: 10240,
      cpuSlowdownMultiplier: 4,
    },
    screenEmulation: {
      mobile: false,
      width: 1366,
      height: 768,
      deviceScaleFactor: 1,
      disabled: false,
    },
  },
};
