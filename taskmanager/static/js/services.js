/**
 * Created by sid on 20/9/17.
 */
angular.module('TaskManagerApp.services', [])
    .service('signUpService', function ($http) {
        var signupFun = function (data) {
            return $http.post('/api/v1/users/', data).then(function (res) {
                return res;
            }, function (err) {
                return err;
            });
        };
        return {
            signUp: signupFun
        };
    })
    .service('signInService', function ($http) {
        var signinFun = function (data) {
            return $http.post('/login/', data).then(function (res) {
                return res;
            }, function (err) {
                return err;
            });
        };
        return {
            signIn: signinFun
        };
    })
    .service('userService', function ($http, $cookieStore) {
        var userData = function (userId) {
            return $http.get('/api/v1/users/' + userId + "/", {
                headers: {
                    'Authorization': 'Token ' + $cookieStore.get('auth_token')
                }
            }).then(function (res) {
                return res;
            }, function (err) {
                return err;
            });
        };

        var taskCreate = function (data) {
            return $http.post('/api/v1/tasks_create/', data, {
                headers: {
                    'Authorization': 'Token ' + $cookieStore.get('auth_token')
                }
            }).then(function (res) {
                return res;
            }, function (err) {
                return err;
            });
        };

        var taskDelete = function (taskId) {
            return $http.delete('/api/v1/tasks_delete/' + taskId + "/", {
                headers: {
                    'Authorization': 'Token ' + $cookieStore.get('auth_token')
                }
            }).then(function (res) {
                return res;
            }, function (err) {
                return err;
            });
        };

        var taskList = function () {
            return $http.get('/api/v1/tasks_list/', {
                headers: {
                    'Authorization': 'Token ' + $cookieStore.get('auth_token')
                }
            }).then(function (res) {
                return res;
            }, function (err) {
                return err;
            });
        };

        var allTaskList = function () {
            return $http.get('/api/v1/tasks_list_all/', {
                headers: {
                    'Authorization': 'Token ' + $cookieStore.get('auth_token')
                }
            }).then(function (res) {
                return res;
            }, function (err) {
                return err;
            });
        };

        var allotTask = function (taskId, students) {
            return $http.post('/api/v1/allot_task/' + taskId + "/", students, {
                headers: {
                    'Authorization': 'Token ' + $cookieStore.get('auth_token')
                }
            }).then(function (res) {
                return res;
            }, function (err) {
                return err;
            });
        };

        var listStudents = function () {
            return $http.get('/api/v1/users/?userprofile__role=STUDENT', {
                headers: {
                    'Authorization': 'Token ' + $cookieStore.get('auth_token')
                }
            }).then(function (res) {
                return res;
            }, function (err) {
                return err;
            });
        };

        var updateStatus = function (task) {
            data = {"status": task.status}
            return $http.patch('/api/v1/tasks_update/' + task.id + "/", data, {
                headers: {
                    'Authorization': 'Token ' + $cookieStore.get('auth_token')
                }
            }).then(function (res) {
                return res;
            }, function (err) {
                return err;
            });
        };


        return {
            userData: userData,
            listStudents: listStudents,
            allotTask: allotTask,
            taskList: taskList,
            taskDelete: taskDelete,
            taskCreate: taskCreate,
            updateStatus: updateStatus,
            allTaskList:allTaskList
        };
    });
