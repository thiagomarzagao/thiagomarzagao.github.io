---
layout: post
title: now on GitHub Pages
comments: true
---

Wordpress.com wouldn't let me have interactive plots, so I just migrated this site to [GitHub Pages](https://pages.github.com/). I believe no permalinks were harmed in the making of this change. All images, videos, and PDFs, must have been ported. And I tested the new layout on Chrome, Firefox, and Safari (IE users: you don't have to live like that) and on iPhone and iPad. But please let me know if you find any issues.

There were some casualties: all comments up to now. Here I'm using [Disqus](https://disqus.com/) to handle comments and, despite heavy googling, I couldn't find a way to export Wordpress.com comments to Disqus (that's possible with Wordpress.org though, by installing a plugin). So, I apologize to all past commenters. And a special apology to all the nice folks who have commented on my [webscraping tutorial](thiagomarzagao.com/2013/11/12/webscraping-with-selenium-part-1/), which is by far the most popular content here (it accounts for way over half the visits) - I love it when people take the time to say it was useful or to provide feedback.

Migrating was pretty easy. I'm using [Jekyll](http://jekyllrb.com/), a Ruby-based generator of static websites. Except for one [pesky dependency](https://github.com/sparklemotion/nokogiri/issues/1235#issuecomment-71693441), installing Jekyll was pretty easy. Theme-wise I forked [Hyde](https://github.com/poole/hyde) (yes, [I see it](http://www.amazon.com/gp/product/0486266885/ref=s9_simh_gw_p14_d0_i2?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=desktop-1&pf_rd_r=1ZSZWY1T4VKT3H5NAV1Z&pf_rd_t=36701&pf_rd_p=1970559082&pf_rd_i=desktop)), which I'm using pretty much unaltered. Most of the work went into migrating the posts. I found [Exitwp](https://github.com/thomasf/exitwp), which by and large automates the task. But I had several posts with code and they gave me some trouble. For instance, Jekyll's own syntax highlighter leaves something to be desired, so I had to [google around](http://demisx.github.io/jekyll/2014/01/13/improve-code-highlighting-in-jekyll.html) to improve it a bit.

Using GitHub Pages has been a pleasant experience so far. I can now do pretty much whatever I want to with my site - which means it's JavaScript time!  I'm also enjoying being able to deploy the site locally before uploading it to GitHub. Jekyll is great too. It lets me write posts in Markdown, which is obviously good for writing math. I wonder how the [Python alternative](http://docs.getpelican.com/en/3.5.0/) compares though, so I may try it out some day.

This is it for now. Posts with interactive plots should follow soon.