from assignment_logic import *
import uuid
import requests
import time
import datetime
import threading

class Client:
    def __init__(self, config):
        self.config = config
        self.context = None
        self.features = {}
        self.running = False

    def add_default_context(self):
        ip_obj = self.get_ip()
        ip = ip_obj["ip"]
        self.context = {"user_id": str(uuid.uuid4()), "ip": ip}

    def update_context(self, context_obj):
        self.context.update(context_obj)

    def get_ip(self):
        response = requests.get("https://ipapi.co/json/")
        return response.json()

    def get_feature_value(self, name):
        feature = next((f for f in self.features["experiments"] + self.features["toggles"] + self.features["rollouts"] if f["name"] == name), None)
        if not feature:
            return False

        if feature["type_id"] != 3:
            return is_enabled(self.features, name, self.context["user_id"])
        else:
            enabled = is_enabled(self.features, name, self.context["user_id"])
            variant = get_variant(self.features, name, self.context["user_id"])
            try:
                users = self.getUsers()
                existingUser = next((user for user in users if user["id"] == self.context["user_id"] and user["variant_id"] == variant["id"]), None)
                if enabled and variant and not existingUser:
                    self.createUser({
                        "id": self.context["user_id"],
                        "variant_id": variant["id"],
                        "ip_address": self.context["ip"]
                    })
            except Exception as e:
                print("Unable to retrieve existing users", e)
            return enabled and variant


    def start(self):
        self.running = True
        while self.running:
            self.fetch_features()
            time.sleep(self.config.interval)

    def stop(self):
        self.running = False

    def start_in_background(self):
        thread = threading.Thread(target=self.start)
        thread.daemon = True
        thread.start()


    def fetch_features(self):
        features = None
        lastModified = datetime.datetime.utcnow() - datetime.timedelta(seconds=self.config.interval / 1000)
        try:
            if not self.features:
                response = requests.get(f"{self.config.server_address}/api/feature/current")
                features = response.json()
                self.features = features
                return features
            else:
                headers = {
                  "If-Modified-Since": lastModified.strftime('%a, %d %b %Y %H:%M:%S GMT')
                }
                url = f"{self.config.server_address}/api/feature/current"
                response = requests.get(url, headers=headers)

                if response.status_code == 304:
                  return self.features
                elif response.status_code == 200:
                  features = response.json()
                  self.features = features
                  return features
                else:
                  print("Error fetching features")
                  return None
        except Exception as e:
            print("Error fetching features:", e)

    def getUsers(self):
        try:
            users = requests.get(f"{self.config.server_address}/api/users")
            return users.json()
        except Exception as e:
            print("Error fetching users:", e)

    def createUser(self, userObj):
        try:
            print(userObj)
            response = requests.post(f"{self.config.server_address}/api/users", json=userObj)
            return response.json()
        except Exception as e:
            print("error creating user", e)
            return e.data

    def createEvent(self, eventObj):
        try:
            response = requests.post(f"{self.config.server_address}/api/events", json=eventObj)
            return response.json()
        except Exception as e:
            return e.data
        

