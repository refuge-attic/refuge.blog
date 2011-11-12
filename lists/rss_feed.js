function(head, req) {
    var Mustache = require("lib/mustache");
    var Markdown = require("lib/markdown");
    
    var ddoc = this;
    var templates = ddoc.templates;
    
    provides("xml", function() {
        var row;
        var posts = [];
        
        while(row = getRow()) {
            var doc = row.value;
            
            var post = doc;
            post.body = Markdown.encode(post.body);
            
            posts.push(post);
        }
        
        return Mustache.to_html(templates.rss_feed, {
            "posts": posts
        });
    });
}