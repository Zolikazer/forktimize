// Base component class - Minimal implementation focusing on render pattern
import type { Component } from './component.interface';

export abstract class BaseComponent<TProps = any> implements Component<TProps> {
  protected props: TProps;

  constructor(props: TProps) {
    this.props = props;
  }

  abstract render(): HTMLElement;
}