module.exports = function (grunt) {
  grunt
    .initConfig({
      "couch-compile": {
        dbs: {
          files: {
            "/tmp/twitter.json": "couchdb/twitter/language"
          }
        }
      },
      "couch-push": {
        options: {
          user: process.env.user,
          pass: process.env.pass
        },
        twitter: {
          files: {
            "http://127.0.0.1:5984/twitter": "/tmp/twitter.json"
          }
        }
      }
    });

  grunt.loadNpmTasks("grunt-couch");
};
