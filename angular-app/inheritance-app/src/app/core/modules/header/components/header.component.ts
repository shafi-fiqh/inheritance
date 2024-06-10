import { Component } from '@angular/core';

@Component({
  selector: 'header-component',
  template: `<header>
  <nav class="bg-white border-gray-200 px-4 lg:px-6 py-2.5 dark:bg-gray-800">
      <div class="flex flex-wrap justify-start items-center mx-auto max-w-screen-xl">
          <a routerLink="/" class="flex items-center">
              <img src="favicon.ico" class="mr-3 h-6 sm:h-9" />
              <span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white">Inheritance</span>
          </a>

      </div>
  </nav>
</header>`,
})
export class HeaderComponent {}
