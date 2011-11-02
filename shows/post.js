function(doc, req) {
    var Mustache = require("lib/mustache");
    var Markdown = require("lib/markdown");
    
    var ddoc = this;
    var templates = ddoc.templates;
    
    provides("html", function() {
        var post = doc;
        post.body = Markdown.encode(post.body);
        var full_post = Mustache.to_html(templates.post_body, post);
        
        return Mustache.to_html(templates.post_page, {
            "post_body": full_post
        });
    });
}