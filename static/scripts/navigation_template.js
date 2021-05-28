/**
 * Creates a custom NavigationBar component. Can be called as a tag using:
 * <nav-bar></nav-bar>
 */
class NavigationBar extends HTMLElement {
  /** Sets the HTML for the NavigationBar element. */
  connectedCallback() {
    this.innerHTML = `
      <ul id="nav-container">
        <li class="link-container"><a class="link" href="/">Home</a></li>
        <li class="link-container"><a class="link" href="/rent">Renting Tools</a></li>
        <li class="link-container"><a class="link" href="/customer">Customer Tools</a></li>
        <li class="link-container"><a class="link" href="/car">Car Tools</a></li>
      </ul>`.trim();
  }
}

customElements.define('nav-bar', NavigationBar);
