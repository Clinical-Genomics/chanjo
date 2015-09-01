var gulp = require('gulp')
var shell = require('gulp-shell')

gulp.task('build-docs', shell.task('make -C docs html'))

gulp.task('default', ['build-docs'], function() {
  gulp.watch(['./docs/*.rst', './docs/*.py'], ['build-docs'])
})
