from constance import config
from sites.models import Site
from api4jenkins import Jenkins as API4Jenkins
from jenkinsapi.jenkins import Jenkins

class JenkinsUtil:
    def __init__(self, site : Site = None):
        self.jenkins_url = config.JENKINS_URL
        self.jenkins_username = config.JENKINS_USERNAME
        self.jenkins_password = config.JENKINS_PASSWORD
        self.site = site
        self.job = None
        

        try:
            self.client = Jenkins(self.jenkins_url, self.jenkins_username, self.jenkins_password)
        except Exception as e:
            raise Exception("Error connecting the Jenkins Client: " + str(e))
        
    def create_job(self):
        if self.site:
            try:
                job_name = self.site["name"]  
                if job_name not in self.client:
                    self.client.create_job(job_name, self._get_job_xml())
                self.job = self.client[job_name]  
            except Exception as e:
                raise Exception("Error creating the job: " + str(e))
        else:
            raise Exception("No Site attribute provided")
        
    def build_job(self):
        """
        Build the Jenkins job.
        """
        if self.job:
            try:
                # Trigger a build for the job
                queue_item = self.job.invoke()
                # Optionally, you can store the build information in your database
                # For example:
                # Build.objects.create(job=self.job.name, number=queue_item.get_number())
                return queue_item
            except Exception as e:
                raise Exception("Error building the job: " + str(e))
        else:
            raise Exception("No job object available")

    def get_all_builds(self):
        """
        Get information about all builds of the Jenkins job.
        """
        if self.job:
            try:
                # Fetch all builds of the job
                builds = self.job.get_build_dict()
                # Optionally, you can process the builds and store information in your database
                # For example:
                # for build_number, build in builds.items():
                #     Build.objects.create(job=self.job.name, number=build_number, result=build.get_status())
                return builds
            except Exception as e:
                raise Exception("Error fetching all builds: " + str(e))
        else:
            raise Exception("No job object available")
    

    def _get_job_xml(self):
        job_xml = """
        <project>
            <description>This is a sample Jenkins job</description>
            <builders>
                <shell>echo "Hello, world!"</shell>
                <shell>echo "ls"</shell>
            </builders>
        </project>
        """
        return job_xml

