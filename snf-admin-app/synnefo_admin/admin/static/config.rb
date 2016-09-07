# Require any additional compass plugins here.

# Set this to the root of your project when deployed:
http_path = "/"
sass_dir = "sass"
images_dir = "images"
css_dir = "css"
# javascripts_dir = "js"

# You can select your preferred output style here (can be overridden via the command line):
# output_style = :nested

# To enable relative paths to assets via compass helper functions. Uncomment:
# relative_assets = true

# To disable debugging comments that display the original location of your selectors. Uncomment:
# line_comments = false


# If you prefer the indented syntax, you might want to regenerate this
# project again passing --syntax sass, or you can uncomment this:
# preferred_syntax = :sass
# and then run:
# sass-convert -R --from scss --to sass sass scss && rm -rf sass && mv scss sass
if environment == :development
    line_comments = true
    output_style = :nested
end

if environment == :production
    line_comments = false
    output_style = :compressed
end 
