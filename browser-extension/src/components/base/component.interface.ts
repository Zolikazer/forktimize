// Component interface - Minimal contract for UI components
export interface Component<TProps = any> {
  render(): HTMLElement;
}