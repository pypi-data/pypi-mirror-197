import argparse
import logging
from base.logger import logger
import os
import yaml

__version__ = "0.1.7"


def load_yaml_data(file):
    with open(file, encoding="utf-8", mode='r') as loader:
        return yaml.safe_load(loader)


def main():
    parser = argparse.ArgumentParser(description="升级打包工具")
    parser.add_argument("-v", "--version", action="version",
                        version=__version__, help="display app version.")
    parser.add_argument("-a", "--apps", help="打包的应用清单，用逗号分隔。")
    parser.add_argument("-d", "--dir", help="应用清单charts目录")
    parser.add_argument("-r", "--registry", help="目标registry")
    parser.add_argument("-n", "--namespace", help="K8s命名空间")
    parser.add_argument("--debug", action="store_true", default=False,
                        help="启用debug模式，会输出更多信息。")

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    apps: str = args.apps
    charts_dir: str = args.dir
    dist_dir = 'dist'
    images_dir = os.path.join(dist_dir, 'images')
    registry = args.registry
    namespace = args.namespace

    logger.info(f'Charts目录:{charts_dir}')
    logger.info(f'需要打包的应用:{apps}')
    if registry is not None:
        logger.info(f'registry={registry}')

    if not os.path.exists(charts_dir):
        logger.error(f'目录不存在:{charts_dir}')
        return

    if not os.path.exists(images_dir):
        os.makedirs(images_dir, exist_ok=True)

    file = open(os.path.join(dist_dir, 'upload.sh'),
                encoding='utf-8', newline='\n', mode='w')
    file.write("#!/bin/bash\n")

    for app in apps.split(','):
        values_file = os.path.join(charts_dir, app, 'values.yaml')
        if not os.path.exists(values_file):
            logger.error(f'应用不存在:{values_file}')
            continue

        try:
            data = load_yaml_data(values_file)
            repository: str = data['image']['repository']
            tag: str = data['image']['tag']

            gz_file = os.path.join(images_dir, app+'.tar.gz')
            img = f'{repository}:{tag}'
            logger.info(f'处理：{img}')

            os.system(f'docker pull {img}')

            if registry is not None:
                r = registry + img[img.index('/'):]
                os.system(f'docker tag {img} {r}')
                img = r
            os.system(f'docker save {img} | gzip > {gz_file}')

            app_dir = os.path.join(charts_dir, app)
            app_file = os.path.join(images_dir, f"{app}.yaml")
            if namespace is not None:
                os.system(
                    f'helm template {app_dir} -n {namespace} > {app_file}')
            else:
                os.system(f'helm template {app_dir} > {app_file}')

            image_file = f"images/{app}.tar.gz"
            file.write(f'docker load < {image_file}\n')
            file.write(f'docker push {img}\n\n')

        except Exception as ex:
            logger.error(ex)
            pass

    file.close()


if __name__ == "__main__":
    main()
