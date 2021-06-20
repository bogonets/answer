var TestData = 
{
  "item" : {
    "project_list" : ["HYUNDAE", "KISCO"],
    "project_name" : "HYUNDAE",
    "user_name" : "bogo",
    "user_email" : "bogo@gmail.com",
    "user_level" : 0,
    "menu_list": [{ "title" : "Layout", "icon": "person", "component" : "v-list-group", "submenu" : [{ "name": "layout1", "icon": "person" }, {"name": "layout2", "icon": "person" }]}, 
                  { "title" : "Event", "icon" : "person", "component" : "v-list-tile"}, 
                  { "title" : "Setting", "icon" : "person", "component" : "v-list-tile"}]
  }
};

var projects_list = 
{
  "item" : {
    "user_name" : "bogo",
    "user_email" : "bogo@gmail.com",
    "user_level" : 0,
    "project_list" : ["HYUNDAE", "KISCO"]
  }
};

var project_list = 
{
  "item" : {
    "user_name" : "bogo",
    "user_email" : "bogo@gmail.com",
    "user_level" : 0,
    "project_list" : ["HYUNDAE"]
  }
};

var project_info = 
{
  "item" : {
    "user_name" : "bogo",
    "user_email" : "bogo@gmail.com",
    "user_level" : 10,
    "project_name" : "HYUNDAE",
    "menu_list" : "0,1,2",
    // "menu_list": [{ "title" : "Layout", "icon": "person", "component" : "v-list-group", "level" : 1, "submenu" : [{ "name": "layout1", "icon": "person" }, {"name": "layout2", "icon": "person" }]}, 
    //               { "title" : "Event", "icon" : "person", "component" : "v-list-tile", "level" : 2}, 
    //               { "title" : "Setting", "icon" : "person", "component" : "v-list-tile", "level" : 3}]
  }
};

var message_info = 
{
  "item" : {
    "message" : ["message1", "message2"],
    "timer": 5000
  }
};

var dashboard_infos = { "layout" : [
                                    {'name': 'layout1', 'panels': [{'x': 0, 'y': 0, 'w': 100, 'h': 100, 'component': null},{'x': 150, 'y': 150, 'w': 100, 'h': 100, 'component': null}]},
                                    {'name': 'layout2', 'panels': [{'x': 150, 'y': 150, 'w': 100, 'h': 100, 'component': null},{'x': 250, 'y': 300, 'w': 150, 'h': 150, 'component': null}]}
                                   ]}

export const getDashboardInfo = async () => {
  return await dashboard_infos;
}

export const getTestInfo = async () => {
  return await TestData;
};

export const getProjectsList = async () => {
  return await projects_list;
};

export const getProjectList = async () => {
  return await project_list;
};

export const getProjectInfo = async () => {
  return await project_info;
};

export const getMessages = async () => {
  return await message_info;
};