from setuptools import setup, find_packages


setup(
    name='streamlit-deeplink',
    version='1.0.0',
    license='MIT',
    description="Streamlit add on to deep link widget selections into url query parameters.",
    author="Karthik Nichenametla",
    author_email='etherxplorer21@example.com',
    packages=find_packages(),
    url='https://github.com/karthik17/streamlit-deeplink',
    python_requires='>=3.6',
    install_requires=[
          'streamlit >= 1.0.0',
      ],

)

