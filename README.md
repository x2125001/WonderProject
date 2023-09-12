# WonderProject
<h1 align="center">Welcome to the Wonder Project 👋</h1>
<p align="center">
  <img src="https://dework.xyz/board.jpeg" />
</p>
<h1 align="center">## Description </h1>
In this Project, thousands of tasks from Dework, the web3-platform are scrapped and analyzed. Specifically, data extraction, ingestion, cleaning & wrangling, KPI analysis, visualization, topic modeling, and bounty regression are implemented.
For Visualization please run the following command under the directory of stremlite:

```sh
streamlit run KPIs.py
```
<p align="center">
  <img src="https://github.com/x2125001/WonderProject/blob/1070631df9a564a6f674a655367716b484226610/pp.png" />
</p>

The results of topic modelling, using the LDA from gensim package will have the yield the following six distinct topics, visualized by the TSNE embeddings 
<p align="center">
  <img src="https://github.com/x2125001/WonderProject/blob/93c36db8fa9a284ac16db6278a8c75b5de6669aa/e.PNG" />
</p>


🚀 Bounty Regression

Using the features of dao, priority, status, tf-idf text features from the task description, and time_to_due, the models of random forest, GradientBoostingRegressor,Ridge Model,KNeighborsRegressor,XGBRegressor, StackingRegressor are fit. The MSE evaluation metric is used, and the achieved average score is 23%. 

Fitted models | boosting_regressor | RandomForest | KNeighborsRegressor | StackingRegressor | Ridge | xgb
--- | --- | --- | --- |--- |--- |--- 
MSE | 0.144 | 0.163 | 0.3086 | 0.2104 | 0.1540 | 0.2134

The best model saved from the  KNeighbors is deployed using the fastapi, which is then integrated into the streamlit 

```sh
npx readme-md-generator
```

Or use default values for all questions (`-y`):

```sh
npx readme-md-generator -y
```

Use your own `ejs` README template (`-p`):

```sh
npx readme-md-generator -p path/to/my/own/template.md
```

You can find [ejs README template examples here](https://github.com/kefranabg/readme-md-generator/tree/master/templates).

## Code Contributors

This project exists thanks to all the people who contribute. [[Contribute](CONTRIBUTING.md)].
<a href="https://github.com/kefranabg/readme-md-generator/graphs/contributors"><img src="https://github.com/x2125001/WonderProject/blob/1070631df9a564a6f674a655367716b484226610/pp.png" /></a>

## Financial Contributors

Become a financial contributor and help us sustain our community. [[Contribute](https://opencollective.com/readme-md-generator/contribute)]

### Individuals

<a href="https://opencollective.com/readme-md-generator"><img src="https://opencollective.com/readme-md-generator/individuals.svg?width=890"></a>

### Organizations

Support this project with your organization. Your logo will show up here with a link to your website. [[Contribute](https://opencollective.com/readme-md-generator/contribute)]
<a href="https://opencollective.com/readme-md-generator/organization/0/website"><img src="https://opencollective.com/readme-md-generator/organization/0/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/1/website"><img src="https://opencollective.com/readme-md-generator/organization/1/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/2/website"><img src="https://opencollective.com/readme-md-generator/organization/2/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/3/website"><img src="https://opencollective.com/readme-md-generator/organization/3/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/4/website"><img src="https://opencollective.com/readme-md-generator/organization/4/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/5/website"><img src="https://opencollective.com/readme-md-generator/organization/5/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/6/website"><img src="https://opencollective.com/readme-md-generator/organization/6/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/7/website"><img src="https://opencollective.com/readme-md-generator/organization/7/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/8/website"><img src="https://opencollective.com/readme-md-generator/organization/8/avatar.svg"></a>
<a href="https://opencollective.com/readme-md-generator/organization/9/website"><img src="https://opencollective.com/readme-md-generator/organization/9/avatar.svg"></a>

## 🤝 Contributing

Contributions, issues and feature requests are welcome.<br />
Feel free to check [issues page](https://github.com/kefranabg/readme-md-generator/issues) if you want to contribute.<br />
[Check the contributing guide](./CONTRIBUTING.md).<br />

## Author

👤 **Franck Abgrall**

- Twitter: [@FranckAbgrall](https://twitter.com/FranckAbgrall)
- Github: [@kefranabg](https://github.com/kefranabg)

## Show your support

Please ⭐️ this repository if this project helped you!

<a href="https://www.patreon.com/FranckAbgrall">
  <img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a>

## 📝 License

Copyright © 2019 [Franck Abgrall](https://github.com/kefranabg).<br />
This project is [MIT](https://github.com/kefranabg/readme-md-generator/blob/master/LICENSE) licensed.

---

_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
