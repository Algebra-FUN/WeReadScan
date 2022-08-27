// @name         Weread Scraper
// @namespace    https://github.com/Sec-ant/weread-scraper
// @version      0.3
// @description  Export Weread books to html file
// @author       Secant

// start observation
contentObserver.observe(document.documentElement, {
    childList: true,
    subtree: true,
});