/**
 * Creates a custom NavigationBar component. Can be called as a tag using:
 * <agent-nav-bar></agent-nav-bar>
 */
 class AgentNavigationBar extends HTMLElement {
  /** Sets the HTML for the NavigationBar element. */
  connectedCallback() {
      this.innerHTML = `
      <nav>
        <div class="logo">
          <p>Database 2: The SQL</p>
        </div>
        <ul id="nav-container">
          <li class="link-container"><a class="link" href="/">Home</a></li>
          <li class="link-container"><a class="link" href="/rent">Renting Tools</a></li>
          <li class="link-container"><a class="link" href="/customer">Customer Tools</a></li>
          <li class="link-container"><a class="link" href="/car">Car Tools</a></li>
        </ul>
      </nav>`.trim();
  }
}

customElements.define('agent-nav-bar', AgentNavigationBar);