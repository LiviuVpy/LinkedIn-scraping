
from get_jobs import GetJobs


if __name__ == "__main__":
    linked_jobs = GetJobs()
    linked_jobs.login()
    input("Press enter after Captcha is solved\n")
    linked_jobs.search_jobs()
    linked_jobs.get_jobs()
    linked_jobs.export_data()

    
