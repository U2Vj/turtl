declare module '@novnc/novnc/core/rfb.js' {
  export default class RFB {
    constructor(target: HTMLElement, url: string);
    scaleViewport: boolean;
    resizeSession: boolean;
    addEventListener(event: string, handler: Function): void;
    removeEventListener(event: string, handler: Function): void;
    disconnect(): void;
    sendCredentials(creds: any): void;
  }
}
