/**
 * Creates a custom NavigationBar component. Can be called as a tag using:
 * <customer-nav-bar></customer-nav-bar>
 */
class CustomerNavigationBar extends HTMLElement {
  /** Sets the HTML for the NavigationBar element. */
  connectedCallback() {
    this.innerHTML = `
      <ul id="nav-container">
        <li class="link-container"><a class="link" href="/">Home</a></li>
        <li class="link-container"><a class="link" href="/rate">Rate Rental</a></li>
        <li class="link-container"><a class="link" href="/login">Agent Portal</a></li>
      </ul>`.trim();
  }
}

customElements.define('customer-nav-bar', CustomerNavigationBar);
